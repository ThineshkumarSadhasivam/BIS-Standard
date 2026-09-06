import re
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.standard import Standard

from app.services.semantic_search_service import semantic_search
from app.services.version_intelligence_service import resolve_standard_version
from app.services.amendment_intelligence_service import get_amendment_history
from app.services.certification_intelligence_service import (
    get_certification_intelligence,
)
from app.services.knowledge_graph_service import get_standard_relationships


# ============================================================
# REGEX PATTERNS
# ============================================================

STANDARD_REFERENCE_PATTERN = re.compile(
    r"\bIS\s+\d+(?:\s*\(Part\s+\d+\))?(?:\s*:\s*\d{4})?",
    re.IGNORECASE,
)

GRADE_PATTERN = re.compile(
    r"\b(33|43|53)\s*grade\b",
    re.IGNORECASE,
)


# ============================================================
# BASIC TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text or ""
    ).strip()


# ============================================================
# PRODUCT / MATERIAL EXTRACTION
# ============================================================

def extract_product(tender_text: str) -> Optional[str]:

    text = tender_text.lower()

    product_patterns = [
        ("cement", [
            "cement",
            "ordinary portland cement",
            "opc",
            "portland cement",
        ]),

        ("aggregate", [
            "aggregate",
            "coarse aggregate",
            "fine aggregate",
        ]),

        ("concrete", [
            "concrete",
            "ready mix concrete",
            "reinforced concrete",
        ]),

        ("steel", [
            "steel",
            "reinforcement steel",
            "reinforcement bar",
            "rebar",
        ]),

        ("brick", [
            "brick",
            "clay brick",
            "burnt clay brick",
        ]),
    ]

    for product, keywords in product_patterns:

        if any(
            keyword in text
            for keyword in keywords
        ):
            return product

    return None


def extract_material(
    tender_text: str
) -> Optional[str]:

    text = tender_text.lower()

    if "cement" in text:
        return "cement"

    if "aggregate" in text:
        return "aggregate"

    if "steel" in text:
        return "steel"

    if "concrete" in text:
        return "concrete"

    if "brick" in text:
        return "brick"

    return None


# ============================================================
# CEMENT TYPE
# ============================================================

def extract_cement_type(
    tender_text: str
) -> Optional[str]:

    text = tender_text.lower()

    if (
        "ordinary portland cement" in text
        or "opc" in text
    ):
        return "ordinary_portland_cement"

    if (
        "portland pozzolana cement" in text
        or "ppc" in text
    ):
        return "portland_pozzolana_cement"

    if (
        "portland slag cement" in text
        or "psc" in text
    ):
        return "portland_slag_cement"

    if "rapid hardening cement" in text:
        return "rapid_hardening_cement"

    if "sulphate resisting cement" in text:
        return "sulphate_resisting_cement"

    return None


# ============================================================
# GRADE
# ============================================================

def extract_grade(
    tender_text: str
) -> Optional[str]:

    match = GRADE_PATTERN.search(
        tender_text or ""
    )

    if match:
        return match.group(1)

    return None


# ============================================================
# APPLICATION
# ============================================================

def extract_application(
    tender_text: str
) -> Optional[str]:

    text = tender_text.lower()

    application_patterns = [
        (
            "building construction",
            [
                "building construction",
                "building works",
                "construction work",
            ],
        ),

        (
            "reinforced concrete construction",
            [
                "reinforced concrete",
                "reinforced concrete structural work",
                "rcc",
            ],
        ),

        (
            "road construction",
            [
                "road construction",
                "road works",
                "highway construction",
            ],
        ),

        (
            "structural construction",
            [
                "structural work",
                "structural construction",
                "structural works",
            ],
        ),
    ]

    for application, keywords in application_patterns:

        if any(
            keyword in text
            for keyword in keywords
        ):
            return application

    return None


# ============================================================
# CERTIFICATION
# ============================================================

CERTIFICATION_TERMS = [
    "bis certification",
    "bis certified",
    "bis licence",
    "bis license",
    "bis mark",
    "isi mark",
    "standard mark",
    "mandatory certification",
    "compulsory certification",
    "certification required",
]


def detect_certification_requirement(
    tender_text: str
) -> bool:

    text = (
        tender_text or ""
    ).lower()

    return any(
        term in text
        for term in CERTIFICATION_TERMS
    )


# ============================================================
# STRUCTURED REQUIREMENTS
# ============================================================

def extract_tender_requirements(
    tender_text: str,
    query_intent=None
) -> Dict:

    product = extract_product(
        tender_text
    )

    material = extract_material(
        tender_text
    )

    cement_type = extract_cement_type(
        tender_text
    )

    grade = extract_grade(
        tender_text
    )

    application = extract_application(
        tender_text
    )

    text = tender_text.lower()

    return {
        "product": product,
        "material": material,
        "cement_type": cement_type,
        "grade": grade,
        "application": application,

        "structural_use": any(
            phrase in text
            for phrase in [
                "structural",
                "reinforced concrete",
                "rcc",
            ]
        ),

        "seismic_requirement": any(
            phrase in text
            for phrase in [
                "seismic",
                "earthquake",
                "earthquake resistant",
            ]
        ),

        "fire_requirement": any(
            phrase in text
            for phrase in [
                "fire resistant",
                "fire resistance",
                "fire safety",
            ]
        ),

        "electrical_requirement": any(
            phrase in text
            for phrase in [
                "electrical",
                "electrical equipment",
            ]
        ),

        "medical_requirement": any(
            phrase in text
            for phrase in [
                "medical",
                "hospital",
                "healthcare",
            ]
        ),

        "standard_type": (
            "Product Specification"
            if "specification" in text
            else None
        ),

        "certification_required":
            detect_certification_requirement(
                tender_text
            ),

        "explicit_standard_references":
            extract_standard_references(
                tender_text
            ),
    }


# ============================================================
# STANDARD REFERENCE EXTRACTION
# ============================================================

def extract_standard_references(
    tender_text: str
) -> List[str]:

    matches = STANDARD_REFERENCE_PATTERN.findall(
        tender_text or ""
    )

    normalized = []

    for match in matches:

        reference = re.sub(
            r"\s+",
            " ",
            match
        ).strip()

        normalized.append(
            reference
        )

    # Deduplicate
    seen = set()
    result = []

    for reference in normalized:

        key = reference.lower()

        if key not in seen:

            seen.add(key)
            result.append(
                reference
            )

    return result


# ============================================================
# PRIMARY STANDARD
# ============================================================

def select_primary_standard(
    search_results: List[Dict]
) -> Optional[Dict]:

    if not search_results:
        return None

    primary = search_results[0]

    score = float(
        primary.get(
            "final_score",
            primary.get(
                "score",
                0.0
            )
        )
    )

    return {
        "id": primary.get("id"),
        "is_number": primary.get("is_number"),
        "title": primary.get("title"),
        "domain": primary.get("domain"),
        "standard_type": primary.get("standard_type"),
        "status": primary.get("status"),

        "confidence": round(
            max(
                0.0,
                min(
                    score,
                    1.0
                )
            ),
            4
        ),
    }


# ============================================================
# VERSION ANALYSIS
# ============================================================

def analyze_version_gap(
    db: Session,
    standard: Standard
) -> Optional[Dict]:

    resolution = resolve_standard_version(
        db,
        standard
    )

    if not resolution:
        return None

    version_status = (
        resolution.get(
            "version_status"
        )
        or ""
    ).lower()

    current_standard = resolution.get(
        "current_standard"
    )

    historical = (
        "historical" in version_status
        or "referenced" in version_status
    )

    if historical:

        return {
            "requirement":
                "Current standard version",

            "status":
                "GAP",

            "severity":
                "HIGH",

            "message": (
                f"{standard.is_number} is a "
                "historical/referenced version. "
                "The current standard should be "
                "used or manually verified."
            ),

            "evidence": {
                "referenced_standard":
                    standard.is_number,

                "current_standard":
                    current_standard,
            },
        }

    return {
        "requirement":
            "Current standard version",

        "status":
            "OK",

        "severity":
            "LOW",

        "message": (
            "The selected standard is not currently "
            "identified as a historical version."
        ),

        "evidence": {
            "standard":
                standard.is_number
        },
    }


# ============================================================
# CERTIFICATION ANALYSIS
# ============================================================

def analyze_certification_gap(
    db: Session,
    standard: Standard,
    certification_required: bool
) -> Optional[Dict]:

    certification = (
        get_certification_intelligence(
            db,
            standard.id
        )
    )

    if not certification:
        return None

    compulsory = certification.get(
        "compulsory",
        False
    )

    if compulsory and certification_required:

        return {
            "requirement":
                "BIS certification",

            "status":
                "FOUND",

            "severity":
                "HIGH",

            "message": (
                "The tender explicitly requires "
                "certification and compulsory BIS "
                "certification evidence exists."
            ),

            "evidence":
                certification,
        }

    if compulsory and not certification_required:

        return {
            "requirement":
                "BIS certification",

            "status":
                "GAP",

            "severity":
                "HIGH",

            "message": (
                "BIS certification is compulsory for "
                "the selected standard, but the tender "
                "does not explicitly mention it."
            ),

            "evidence":
                certification,
        }

    if certification_required:

        return {
            "requirement":
                "BIS certification",

            "status":
                "REVIEW",

            "severity":
                "MEDIUM",

            "message": (
                "The tender requires certification, "
                "but compulsory certification evidence "
                "was not found in the current dataset."
            ),

            "evidence":
                certification,
        }

    return {
        "requirement":
            "BIS certification",

        "status":
            "NO_EVIDENCE",

        "severity":
            "LOW",

        "message": (
            "No certification evidence is currently "
            "recorded in the dataset."
        ),

        "evidence":
            certification,
    }


# ============================================================
# GRADE GAP
# ============================================================

def analyze_grade_gap(
    standard: Standard,
    requirements: Dict
) -> Optional[Dict]:

    product = requirements.get(
        "product"
    )

    grade = requirements.get(
        "grade"
    )

    if product != "cement":
        return None

    if grade:
        return {
            "requirement":
                "Cement grade",

            "status":
                "FOUND",

            "severity":
                "MEDIUM",

            "message":
                f"Cement grade {grade} is explicitly specified.",

            "evidence": {
                "grade":
                    grade
            },
        }

    return {
        "requirement":
            "Cement grade",

        "status":
            "GAP",

        "severity":
            "MEDIUM",

        "message": (
            "Cement grade is not explicitly specified "
            "in the tender. The required grade should "
            "be verified before procurement."
        ),

        "evidence": {
            "standard":
                standard.is_number
        },
    }


# ============================================================
# AMENDMENT ANALYSIS
# ============================================================

def analyze_amendments(
    db: Session,
    standard: Standard
) -> Optional[Dict]:

    history = get_amendment_history(
        db,
        standard.id
    )

    if not history:
        return None

    count = history.get(
        "amendment_count",
        0
    )

    latest = history.get(
        "latest_amendment"
    )

    if count > 0:

        return {
            "requirement":
                "Amendment awareness",

            "status":
                "REVIEW",

            "severity":
                "MEDIUM",

            "message": (
                f"{count} amendment(s) are recorded "
                "for this standard. The applicable "
                "amendments should be considered."
            ),

            "evidence": {
                "amendment_count":
                    count,

                "latest_amendment":
                    latest,
            },
        }

    return {
        "requirement":
            "Amendment awareness",

        "status":
            "NO_EVIDENCE",

        "severity":
            "LOW",

        "message": (
            "No amendments are currently recorded "
            "for this standard in the verified dataset."
        ),

        "evidence":
            history,
    }


# ============================================================
# EXPLICIT STANDARD VALIDATION
# ============================================================

def validate_explicit_references(
    db: Session,
    references: List[str]
) -> List[Dict]:

    results = []

    for reference in references:

        standard = (
            db.query(Standard)
            .filter(
                Standard.is_number.ilike(
                    reference
                )
            )
            .first()
        )

        if standard:

            resolution = resolve_standard_version(
                db,
                standard
            )

            results.append({
                "reference":
                    reference,

                "status":
                    "FOUND",

                "standard_id":
                    standard.id,

                "title":
                    standard.title,

                "version_intelligence":
                    resolution,
            })

        else:

            results.append({
                "reference":
                    reference,

                "status":
                    "NOT_FOUND",

                "message": (
                    "The referenced standard could not "
                    "be matched in the current dataset."
                ),
            })

    return results


# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

def analyze_related_standards(
    db: Session,
    standard: Standard
) -> Optional[Dict]:

    graph = get_standard_relationships(
        db,
        standard.id
    )

    if not graph:
        return None

    categories = graph.get(
        "categories",
        {}
    )

    return {
        "relationship_count":
            graph.get(
                "relationship_count",
                0
            ),

        "category_counts":
            graph.get(
                "category_counts",
                {}
            ),

        "test_references":
            categories.get(
                "test_references",
                []
            ),

        "material_references":
            categories.get(
                "material_references",
                []
            ),

        "conformity_inputs":
            categories.get(
                "conformity_inputs",
                []
            ),

        "referenced_standards":
            categories.get(
                "referenced_standards",
                []
            ),
    }


# ============================================================
# HUMAN REVIEW DECISION
# ============================================================

def determine_human_review(
    primary: Optional[Dict],
    gaps: List[Dict],
    explicit_references: List[Dict]
) -> Dict:

    reasons = []

    if not primary:

        reasons.append(
            "No primary standard was identified."
        )

    else:

        confidence = primary.get(
            "confidence",
            0.0
        )

        if confidence < 0.60:

            reasons.append(
                "Primary standard confidence is below 0.60."
            )

    if any(
        gap.get("severity") == "HIGH"
        and gap.get("status") == "GAP"
        for gap in gaps
    ):

        reasons.append(
            "A high-severity procurement gap was detected."
        )

    if any(
        reference.get("status") == "NOT_FOUND"
        for reference in explicit_references
    ):

        reasons.append(
            "An explicitly referenced standard could not "
            "be resolved in the dataset."
        )

    return {
        "required":
            len(reasons) > 0,

        "reasons":
            reasons,
    }


# ============================================================
# MAIN TENDER ANALYSIS
# ============================================================

def analyze_tender(
    db: Session,
    tender_text: str,
    top_k: int = 5
) -> Dict:

    tender_text = normalize_text(
        tender_text
    )

    # --------------------------------------------------------
    # STEP 1 — Semantic Search
    # --------------------------------------------------------

    search_results = semantic_search(
        db,
        tender_text,
        top_k
    )

    # --------------------------------------------------------
    # STEP 2 — Requirements
    # --------------------------------------------------------

    requirements = extract_tender_requirements(
        tender_text
    )

    # --------------------------------------------------------
    # STEP 3 — Primary Standard
    # --------------------------------------------------------

    primary = select_primary_standard(
        search_results
    )

    # --------------------------------------------------------
    # STEP 4 — Explicit References
    # --------------------------------------------------------

    explicit_references = (
        validate_explicit_references(
            db,
            requirements[
                "explicit_standard_references"
            ]
        )
    )

    # --------------------------------------------------------
    # NO RESULT CASE
    # --------------------------------------------------------

    if not primary:

        review = determine_human_review(
            None,
            [],
            explicit_references
        )

        return {
            "tender_text":
                tender_text,

            "requirements_detected":
                requirements,

            "primary_standard":
                None,

            "candidate_standards":
                search_results,

            "explicit_standard_validation":
                explicit_references,

            "gaps":
                [],

            "related_standards":
                {},

            "human_review_required":
                review["required"],

            "review_reasons":
                review["reasons"],

            "analysis_scope":
                "Metadata-level procurement analysis; "
                "not clause-level compliance verification.",
        }

    # --------------------------------------------------------
    # STEP 5 — Resolve Database Standard
    # --------------------------------------------------------

    standard = (
        db.query(Standard)
        .filter(
            Standard.is_number
            == primary["is_number"]
        )
        .first()
    )

    if not standard:

        review = determine_human_review(
            primary,
            [],
            explicit_references
        )

        return {
            "tender_text":
                tender_text,

            "requirements_detected":
                requirements,

            "primary_standard":
                primary,

            "candidate_standards":
                search_results,

            "explicit_standard_validation":
                explicit_references,

            "gaps":
                [],

            "related_standards":
                {},

            "human_review_required":
                True,

            "review_reasons":
                review["reasons"]
                + [
                    "Primary standard could not be "
                    "resolved in the database."
                ],

            "analysis_scope":
                "Metadata-level procurement analysis; "
                "not clause-level compliance verification.",
        }

    # --------------------------------------------------------
    # STEP 6 — Gap Analysis
    # --------------------------------------------------------

    gaps = []

    version_gap = analyze_version_gap(
        db,
        standard
    )

    if version_gap:
        gaps.append(
            version_gap
        )

    certification_gap = analyze_certification_gap(
        db,
        standard,
        requirements[
            "certification_required"
        ]
    )

    if certification_gap:
        gaps.append(
            certification_gap
        )

    grade_gap = analyze_grade_gap(
        standard,
        requirements
    )

    if grade_gap:
        gaps.append(
            grade_gap
        )

    amendment_gap = analyze_amendments(
        db,
        standard
    )

    if amendment_gap:
        gaps.append(
            amendment_gap
        )

    # --------------------------------------------------------
    # STEP 7 — Knowledge Graph
    # --------------------------------------------------------

    related_standards = (
        analyze_related_standards(
            db,
            standard
        )
    )

    # --------------------------------------------------------
    # STEP 8 — Human Review
    # --------------------------------------------------------

    review = determine_human_review(
        primary,
        gaps,
        explicit_references
    )

    # --------------------------------------------------------
    # STEP 9 — Audit Trail
    # --------------------------------------------------------

    audit_trail = [
        "tender_received",
        "requirements_extracted",
        "semantic_search_completed",
        "primary_standard_selected",
        "explicit_references_validated",
        "version_checked",
        "certification_checked",
        "amendments_checked",
        "knowledge_graph_traversed",
        "gap_analysis_completed",
        "human_review_decision_generated",
    ]

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {
        "tender_text":
            tender_text,

        "requirements_detected":
            requirements,

        "primary_standard":
            primary,

        "candidate_standards":
            search_results,

        "explicit_standard_validation":
            explicit_references,

        "gaps":
            gaps,

        "related_standards":
            related_standards,

        "human_review_required":
            review["required"],

        "review_reasons":
            review["reasons"],

        "audit_trail":
            audit_trail,

        "analysis_scope":
            "Metadata-level procurement analysis; "
            "not clause-level compliance verification.",
    }