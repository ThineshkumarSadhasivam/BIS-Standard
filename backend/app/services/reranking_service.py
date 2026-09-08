import re
from typing import List, Dict, Optional


# =========================================================
# STOP WORDS
# =========================================================

STOP_WORDS = {
    "the",
    "a",
    "an",
    "for",
    "of",
    "and",
    "or",
    "to",
    "in",
    "on",
    "with",
    "used",
    "use",
    "requirements",
    "requirement",
}


# =========================================================
# RERANKING WEIGHTS
# =========================================================

SEMANTIC_WEIGHT = 0.45
TITLE_WEIGHT = 0.15
DOMAIN_WEIGHT = 0.10
TYPE_WEIGHT = 0.05
PHRASE_WEIGHT = 0.10
STATUS_WEIGHT = 0.05
ATTRIBUTE_WEIGHT = 0.10

# Additional product-category adjustment.
# This is deliberately applied only when a strong product category
# can be inferred from the procurement query.
PRODUCT_CATEGORY_BOOST = 0.18
PRODUCT_CATEGORY_PENALTY = 0.18


# =========================================================
# IMPORTANT PHRASES
# =========================================================

IMPORTANT_PHRASES = [
    "plain and reinforced concrete",
    "reinforced concrete",
    "ordinary portland cement",
    "portland slag cement",
    "portland pozzolana cement",
    "53 grade",
    "43 grade",
    "33 grade",
    "coarse aggregate",
    "fine aggregate",
    "concrete aggregate",
    "structural concrete",
    "code of practice",
    "product specification",
    # Electrical / cable phrases
    "electrical cable",
    "power cable",
    "power cables",
    "electrical wiring",
    "pvc insulated cable",
    "xlpe cable",
    "1100 v cable",
    "1100v cable",
]


# =========================================================
# TOKENIZATION
# =========================================================

def tokenize(text: str) -> List[str]:
    if not text:
        return []

    text = text.lower()

    tokens = re.findall(r"[a-z0-9]+", text)

    return [
        token
        for token in tokens
        if token not in STOP_WORDS
    ]


# =========================================================
# TITLE MATCHING
# =========================================================

def lexical_title_score(query: str, title: str) -> float:
    query_tokens = set(tokenize(query))
    title_tokens = set(tokenize(title))

    if not query_tokens or not title_tokens:
        return 0.0

    overlap = query_tokens.intersection(title_tokens)

    return len(overlap) / len(query_tokens)


# =========================================================
# PHRASE MATCHING
# =========================================================

def phrase_match_score(query: str, title: str) -> float:
    if not query or not title:
        return 0.0

    query_lower = query.lower()
    title_lower = title.lower()

    matches = 0

    for phrase in IMPORTANT_PHRASES:
        if phrase in query_lower and phrase in title_lower:
            matches += 1

    if matches == 0:
        return 0.0

    return min(matches * 0.5, 1.0)


# =========================================================
# DOMAIN MATCHING
# =========================================================

def domain_score(query: str, domain: str) -> float:
    query_tokens = set(tokenize(query))
    domain_tokens = set(tokenize(domain))

    if not query_tokens or not domain_tokens:
        return 0.0

    overlap = query_tokens.intersection(domain_tokens)

    return min(
        len(overlap) / len(query_tokens),
        1.0,
    )


# =========================================================
# STANDARD TYPE MATCHING
# =========================================================

def standard_type_score(query: str, standard_type: str) -> float:
    query_lower = query.lower()
    standard_type_lower = (standard_type or "").lower()

    score = 0.0

    if "specification" in query_lower:
        if "specification" in standard_type_lower:
            score = 1.0

    if "test" in query_lower:
        if "test" in standard_type_lower:
            score = 1.0

    if "code of practice" in query_lower:
        if "code of practice" in standard_type_lower:
            score = 1.0

    if "guideline" in query_lower:
        if "guideline" in standard_type_lower:
            score = 1.0

    return score


# =========================================================
# STATUS MATCHING
# =========================================================

def status_score(status: str) -> float:
    status_lower = (status or "").lower()

    if (
        "active/current" in status_lower
        or "active" in status_lower
        or "current" in status_lower
    ):
        return 1.0

    if "historical" in status_lower:
        return -1.0

    if "referenced" in status_lower:
        return -0.5

    return 0.0


# =========================================================
# PRODUCT CATEGORY INFERENCE
# =========================================================

def infer_electrical_product(
    query: str,
    query_intent=None,
) -> Optional[str]:
    """
    Infer the electrical product category from the procurement query.

    This intentionally uses the raw query as a fallback because the
    current QueryIntent model may not yet contain an electrical_product
    field. Therefore this reranker remains backward-compatible with the
    existing NLP / query-intent implementation.
    """

    explicit_category = getattr(
        query_intent,
        "electrical_product",
        None,
    )

    if explicit_category:
        return explicit_category

    text = (query or "").lower()

    cable_terms = [
        "electrical cable",
        "electrical cables",
        "power cable",
        "power cables",
        "pvc insulated cable",
        "pvc insulated cables",
        "xlpe cable",
        "xlpe cables",
        "armoured cable",
        "armoured cables",
        "unarmoured cable",
        "unarmoured cables",
        "cable wiring",
        "cable for power distribution",
        "cables for power distribution",
    ]

    if any(term in text for term in cable_terms):
        return "cable"

    # A plain "cable/cables" mention is already strong evidence for
    # the product category, especially in procurement specifications.
    if re.search(r"\bcables?\b", text):
        return "cable"

    # "wire" is accepted only with electrical/wiring context to avoid
    # unrelated wire products.
    if (
        re.search(r"\bwires?\b", text)
        and any(
            term in text
            for term in [
                "electrical",
                "power distribution",
                "electrical installation",
                "wiring",
                "conductor",
                "voltage",
            ]
        )
    ):
        return "cable"

    return None


# =========================================================
# PRODUCT CATEGORY MATCHING
# =========================================================

def product_category_score(
    query: str,
    result: Dict,
    query_intent=None,
) -> float:
    """
    Return product-category compatibility in the range [-1, 1].

    This is separate from the generic semantic score. Semantic search
    can correctly identify that two products are both electrical/safety
    related, while procurement relevance requires a stronger product
    constraint. For example, a PV module safety standard should not
    outrank a cable specification for a cable procurement query.
    """

    electrical_product = infer_electrical_product(
        query,
        query_intent,
    )

    if electrical_product != "cable":
        return 0.0

    title = (result.get("title", "") or "").lower()
    domain = (result.get("domain", "") or "").lower()

    cable_title = any(
        term in title
        for term in [
            "cable",
            "cables",
            "cords",
            "wire",
            "wires",
        ]
    )

    cable_domain = any(
        term in domain
        for term in [
            "cable",
            "cables",
            "wiring",
            "power cable",
        ]
    )

    # Strong positive signal: the standard itself is about cables/wiring.
    if cable_title and cable_domain:
        return 1.0

    if cable_title:
        return 0.90

    if cable_domain:
        return 0.85

    # These are electrical products, but they are not the requested
    # cable product category. Penalize them so semantic similarity does
    # not incorrectly make them the primary recommendation.
    unrelated_domains = [
        "solar pv",
        "photovoltaic",
        "electrical appliances",
        "electrical appliance",
        "electrical motors",
        "rotating electrical machines",
        "switchgear",
        "electronics",
        "ict",
        "transformer",
        "lighting",
    ]

    if any(term in domain for term in unrelated_domains):
        return -1.0

    unrelated_title_terms = [
        "photovoltaic",
        "pv module",
        "solar module",
        "rotating electrical machine",
        "electric motor",
        "household appliance",
        "switchgear",
    ]

    if any(term in title for term in unrelated_title_terms):
        return -1.0

    # Generic electrical standards remain possible supporting standards,
    # but should not beat a direct cable product standard.
    if any(
        term in title or term in domain
        for term in ["electrical", "electric"]
    ):
        return -0.25

    return -0.50


# =========================================================
# ATTRIBUTE MATCHING
# =========================================================

def attribute_match_score(
    query_intent,
    result: Dict,
) -> float:
    """
    Compare structured procurement intent against a retrieved Indian
    Standard.

    Strong positive:
        Explicitly matches requested attribute.

    Small positive:
        Broad/general compatibility.

    Negative:
        Specialized or conflicting candidate.

    Product-category compatibility for electrical cables is handled here
    as well as by the final product-category adjustment. The duplicated
    signal is intentional: attribute scoring supports the existing
    feature model, while product_category_score provides a stronger
    procurement-category gate.
    """

    title = (result.get("title", "") or "").lower()
    domain = (result.get("domain", "") or "").lower()
    standard_type = (result.get("standard_type", "") or "").lower()

    score = 0.0

    # =====================================================
    # QUERY ATTRIBUTES
    # =====================================================

    product = getattr(query_intent, "product", None)
    cement_type = getattr(query_intent, "cement_type", None)
    requested_grade = getattr(query_intent, "grade", None)
    application = getattr(query_intent, "application", None)
    structural_use = getattr(query_intent, "structural_use", False)
    seismic_requirement = getattr(query_intent, "seismic_requirement", False)
    fire_requirement = getattr(query_intent, "fire_requirement", False)
    electrical_requirement = getattr(query_intent, "electrical_requirement", False)
    requested_standard_type = getattr(query_intent, "standard_type", None)

    # =====================================================
    # PRODUCT MATCH
    # =====================================================

    if product == "cement":
        if "cement" in title or "cement" in domain:
            score += 0.75
        else:
            score -= 2.0

        specialized_terms = [
            "high alumina",
            "masonry cement",
            "white portland",
            "hydrophobic",
            "low heat",
            "composite cement",
            "pozzolana",
            "portland slag",
            "rapid hardening",
            "microfine",
            "calcined clay",
            "limestone cement",
        ]

        if cement_type:
            requested_terms = {
                "ordinary portland cement": [
                    "ordinary portland cement",
                    "opc",
                ],
                "portland slag cement": [
                    "portland slag cement",
                    "psc",
                ],
                "portland pozzolana cement": [
                    "portland pozzolana cement",
                    "pozzolana",
                    "ppc",
                ],
            }

            requested_keywords = requested_terms.get(
                cement_type,
                [],
            )

            requested_specialization = any(
                keyword in title
                for keyword in requested_keywords
            )

            if requested_specialization:
                score += 2.0
            else:
                score -= 1.0

        if not cement_type:
            has_specialized_cement = any(
                term in title
                for term in specialized_terms
            )

            if has_specialized_cement:
                score -= 1.5

            if "ordinary portland cement" in title:
                score += 1.0

        if cement_type == "ordinary portland cement":
            if "ordinary portland cement" in title:
                score += 2.0

            for term in specialized_terms:
                if term in title:
                    score -= 1.25
                    break

    # =====================================================
    # AGGREGATE
    # =====================================================

    elif product == "aggregate":
        if "aggregate" in title:
            score += 2.0
        else:
            score -= 2.0

    # =====================================================
    # STEEL
    # =====================================================

    elif product == "steel":
        if "steel" in title:
            score += 2.0
        else:
            score -= 2.0

    # =====================================================
    # CONCRETE
    # =====================================================

    elif product == "concrete":
        if "concrete" in title:
            score += 1.0
        else:
            score -= 2.0

        if (
            "steel bar" in title
            or "steel bars" in title
            or "reinforcement" in title
        ):
            score -= 1.25

    # =====================================================
    # BRICK
    # =====================================================

    elif product == "brick":
        if "brick" in title:
            score += 2.0
        else:
            score -= 2.0

    # =====================================================
    # MEDICAL TEXTILE
    # =====================================================

    elif product == "medical_textile":
        if (
            "medical" in title
            or "textile" in title
            or "coverall" in title
        ):
            score += 2.0
        else:
            score -= 2.0

    # =====================================================
    # ELECTRICAL CABLE
    # =====================================================

    electrical_product = infer_electrical_product(
        getattr(query_intent, "raw_query", None) or "",
        query_intent,
    )

    # raw_query may not exist on every QueryIntent implementation.
    # Fall back to the result-independent query later through the final
    # product-category feature.
    if electrical_product == "cable":
        if "cable" in title or "cables" in title:
            score += 3.0
        elif "wire" in title or "wiring" in title:
            score += 1.0
        else:
            score -= 2.0

        if any(
            term in domain
            for term in [
                "cable",
                "cables",
                "wiring",
            ]
        ):
            score += 2.5

        unrelated_domains = [
            "solar pv",
            "photovoltaic",
            "electrical appliances",
            "electrical appliance",
            "electrical motors",
            "rotating electrical machines",
            "switchgear",
            "electronics",
            "ict",
        ]

        if any(domain_name in domain for domain_name in unrelated_domains):
            score -= 3.0

        unrelated_title_terms = [
            "photovoltaic",
            "pv module",
            "solar module",
            "electric motor",
            "rotating electrical machine",
            "household appliance",
            "switchgear",
        ]

        if any(term in title for term in unrelated_title_terms):
            score -= 3.0

    # =====================================================
    # GRADE MATCH
    # =====================================================

    if requested_grade:
        requested_grade_pattern = rf"\b{re.escape(str(requested_grade))}\s*grade\b"

        if re.search(requested_grade_pattern, title):
            score += 3.0

        other_grades = {"33", "43", "53"} - {str(requested_grade)}

        for grade in other_grades:
            if re.search(rf"\b{grade}\s*grade\b", title):
                score -= 3.0
                break

    # =====================================================
    # APPLICATION
    # =====================================================

    if application:
        if application == "plain and reinforced concrete":
            if "plain and reinforced concrete" in title:
                score += 2.5
            elif "reinforced concrete" in title and "plain" in title:
                score += 1.5

        elif application == "reinforced concrete":
            if "reinforced concrete" in title:
                score += 1.25
            elif "concrete" in title:
                score += 0.25

        elif application == "plain concrete":
            if "plain concrete" in title:
                score += 1.5

        elif application == "structural concrete":
            if "structural concrete" in title:
                score += 1.5
            elif "concrete" in title:
                score += 0.25

        elif application == "building construction":
            if "building" in title or "construction" in title:
                score += 0.5

        # Electrical installation / power distribution application.
        elif application in {
            "electrical installation",
            "building electrical installation",
            "power distribution",
            "electrical power distribution",
        }:
            if any(
                term in title or term in domain
                for term in [
                    "cable",
                    "cables",
                    "wiring",
                    "power distribution",
                    "electrical installation",
                ]
            ):
                score += 1.5

    # =====================================================
    # STRUCTURAL USE
    # =====================================================

    if structural_use:
        if (
            "structural use" in title
            or "structural concrete" in title
            or "reinforced concrete" in title
            or "plain and reinforced concrete" in title
        ):
            score += 0.25

    # =====================================================
    # SEISMIC REQUIREMENT
    # =====================================================

    seismic_terms = [
        "seismic",
        "earthquake",
        "ductile",
    ]

    title_is_seismic = any(
        term in title
        for term in seismic_terms
    )

    if seismic_requirement:
        if title_is_seismic:
            score += 2.5
    else:
        if title_is_seismic:
            score -= 2.5

    # =====================================================
    # FIRE REQUIREMENT
    # =====================================================

    fire_terms = [
        "fire",
        "fire resistance",
        "fire resistant",
        "fire-resistant",
        "flame retardant",
        "flame-retardant",
        "halogen-free flame-retardant",
    ]

    title_is_fire_related = any(
        term in title
        for term in fire_terms
    )

    if fire_requirement:
        if title_is_fire_related:
            score += 1.5

    # =====================================================
    # ELECTRICAL REQUIREMENT
    # =====================================================

    if electrical_requirement:
        electrical_terms = [
            "electrical",
            "electric",
            "cable",
            "cables",
            "wiring",
            "power",
        ]

        if any(term in title for term in electrical_terms):
            score += 1.5

        if any(term in domain for term in electrical_terms):
            score += 0.75

    # =====================================================
    # STANDARD TYPE
    # =====================================================

    if requested_standard_type:
        if requested_standard_type == "specification":
            if "specification" in standard_type:
                score += 0.75

        elif requested_standard_type == "code_of_practice":
            if "code of practice" in standard_type:
                score += 0.75

        elif requested_standard_type == "test_method":
            if "test" in standard_type:
                score += 0.75

        elif requested_standard_type == "guideline":
            if "guideline" in standard_type:
                score += 0.75

    # =====================================================
    # TEST METHODS
    # =====================================================

    # Test methods are generally supporting/related standards, not
    # primary product specifications, unless testing is requested.
    if (
        "test" in standard_type
        and requested_standard_type != "test_method"
    ):
        score -= 0.5

    return score


# =========================================================
# FINAL SCORE
# =========================================================

def calculate_final_score(
    query: str,
    result: Dict,
    query_intent=None,
) -> Dict:
    # =====================================================
    # SEMANTIC
    # =====================================================

    semantic_score = float(
        result.get("score", 0.0)
    )

    # =====================================================
    # TITLE
    # =====================================================

    title_score = lexical_title_score(
        query,
        result.get("title", ""),
    )

    # =====================================================
    # DOMAIN
    # =====================================================

    domain_match = domain_score(
        query,
        result.get("domain", ""),
    )

    # =====================================================
    # STANDARD TYPE
    # =====================================================

    type_match = standard_type_score(
        query,
        result.get("standard_type", ""),
    )

    # =====================================================
    # PHRASE
    # =====================================================

    phrase_match = phrase_match_score(
        query,
        result.get("title", ""),
    )

    # =====================================================
    # STATUS
    # =====================================================

    status_match = status_score(
        result.get("status", ""),
    )

    # =====================================================
    # ATTRIBUTE
    # =====================================================

    if query_intent is not None:
        attribute_score = attribute_match_score(
            query_intent,
            result,
        )

        attribute_score_normalized = max(
            -1.0,
            min(attribute_score / 4.0, 1.0),
        )
    else:
        attribute_score = 0.0
        attribute_score_normalized = 0.0

    # =====================================================
    # PRODUCT CATEGORY
    # =====================================================

    category_match = product_category_score(
        query,
        result,
        query_intent,
    )

    # =====================================================
    # ORIGINAL HYBRID SCORE
    # =====================================================

    base_score = (
        SEMANTIC_WEIGHT * semantic_score
        + TITLE_WEIGHT * title_score
        + DOMAIN_WEIGHT * domain_match
        + TYPE_WEIGHT * type_match
        + PHRASE_WEIGHT * phrase_match
        + STATUS_WEIGHT * status_match
        + ATTRIBUTE_WEIGHT * attribute_score_normalized
    )

    # =====================================================
    # PRODUCT-AWARE ADJUSTMENT
    # =====================================================

    product_adjustment = 0.0

    if category_match >= 0.80:
        product_adjustment = PRODUCT_CATEGORY_BOOST
    elif category_match <= -0.80:
        product_adjustment = -PRODUCT_CATEGORY_PENALTY
    elif category_match < 0:
        product_adjustment = PRODUCT_CATEGORY_PENALTY * category_match

    final_score = base_score + product_adjustment

    # Keep displayed confidence within a conventional 0-1 range.
    final_score = max(0.0, min(final_score, 1.0))

    # =====================================================
    # COPY RESULT
    # =====================================================

    result = result.copy()

    result["semantic_score"] = round(semantic_score, 4)
    result["title_score"] = round(title_score, 4)
    result["domain_score"] = round(domain_match, 4)
    result["type_score"] = round(type_match, 4)
    result["phrase_score"] = round(phrase_match, 4)
    result["status_score"] = round(status_match, 4)
    result["attribute_score"] = round(attribute_score, 4)

    # New explainability fields.
    result["product_category"] = infer_electrical_product(
        query,
        query_intent,
    )
    result["product_category_score"] = round(category_match, 4)
    result["product_category_adjustment"] = round(
        product_adjustment,
        4,
    )

    result["base_score"] = round(base_score, 4)
    result["final_score"] = round(final_score, 4)

    return result


# =========================================================
# RERANK
# =========================================================

def rerank_results(
    query: str,
    results: List[Dict],
    query_intent=None,
) -> List[Dict]:
    reranked = [
        calculate_final_score(
            query=query,
            result=result,
            query_intent=query_intent,
        )
        for result in results
    ]

    # Highest final score first.
    reranked.sort(
        key=lambda item: item["final_score"],
        reverse=True,
    )

    # Reassign ranking after product-aware reranking.
    for rank, result in enumerate(
        reranked,
        start=1,
    ):
        result["rank"] = rank

    return reranked
