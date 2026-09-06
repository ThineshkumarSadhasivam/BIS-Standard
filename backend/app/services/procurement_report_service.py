from typing import Any, Dict, List, Optional


# ============================================================
# HELPERS
# ============================================================

def _severity_rank(value: str) -> int:
    return {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }.get((value or "").upper(), 0)


def _standard_snapshot(standard: Optional[Dict]) -> Optional[Dict]:
    """
    Keep only procurement-relevant fields from a standard object.
    """
    if not isinstance(standard, dict):
        return None

    return {
        "id": standard.get("id"),
        "is_number": standard.get("is_number"),
        "title": standard.get("title"),
        "domain": standard.get("domain"),
        "standard_type": standard.get("standard_type"),
        "status": standard.get("status"),
        "confidence": standard.get("confidence"),
    }


def _build_why_recommended(analysis: Dict) -> List[str]:
    """
    Build human-readable reasons from the already extracted
    tender requirements and selected primary standard.
    """
    reasons: List[str] = []

    primary = analysis.get("primary_standard") or {}
    requirements = analysis.get("requirements_detected") or {}

    if primary.get("is_number"):
        reasons.append(
            f"Highest-ranked semantic candidate: "
            f"{primary['is_number']}."
        )

    if requirements.get("product"):
        reasons.append(
            f"Product identified as "
            f"{requirements['product']}."
        )

    if requirements.get("material"):
        reasons.append(
            f"Material identified as "
            f"{requirements['material']}."
        )

    if requirements.get("cement_type"):
        reasons.append(
            f"Cement type detected as "
            f"{requirements['cement_type']}."
        )

    if requirements.get("grade"):
        reasons.append(
            f"Grade requirement detected: "
            f"{requirements['grade']}."
        )

    if requirements.get("application"):
        reasons.append(
            f"Application detected as "
            f"{requirements['application']}."
        )

    if requirements.get("explicit_standard_references"):
        reasons.append(
            "Explicit BIS standard references were separately "
            "validated to avoid silently replacing cited standards."
        )

    return reasons


# ============================================================
# COMPLIANCE
# ============================================================

def _build_compliance_section(analysis: Dict) -> Dict:
    """
    Build the compliance section from the enriched primary
    standard produced by tender_analysis_service.py.

    The tender analysis must enrich primary_standard with:
        compliance_intelligence
        version_intelligence
        amendment_intelligence
        certification_intelligence
        source_document
        source_url
        source_authority
        source_type
    """

    primary = analysis.get("primary_standard") or {}

    compliance = (
        primary.get("compliance_intelligence")
        or {}
    )

    certification = (
        primary.get("certification_intelligence")
        or {}
    )

    version = (
        primary.get("version_intelligence")
        or {}
    )

    amendments = (
        primary.get("amendment_intelligence")
        or {}
    )

    # --------------------------------------------------------
    # If compliance intelligence exists, use it as authority.
    # --------------------------------------------------------

    if compliance:
        return {
            "status": compliance.get(
                "overall_compliance_status"
            ),
            "qco_applicable": compliance.get(
                "qco_applicable"
            ),
            "isi_mark_required": compliance.get(
                "isi_mark_required"
            ),
            "is_latest_version": compliance.get(
                "is_latest_version"
            ),
            "recommended_standard": compliance.get(
                "recommended_standard"
            ) or _standard_snapshot(primary),
            "latest_amendment_year": compliance.get(
                "latest_amendment_year"
            ),
            "recommendation": compliance.get(
                "recommendation"
            ),
        }

    # --------------------------------------------------------
    # Defensive fallback:
    # build useful compliance information from the individual
    # intelligence objects if the combined service was not added.
    # --------------------------------------------------------

    certification_status = (
        certification.get("overall_status")
        or certification.get("overall_compliance_status")
    )

    if certification_status:
        compulsory = certification.get(
            "compulsory"
        )

        return {
            "status": (
                "Compulsory"
                if compulsory is True
                else certification_status
            ),
            "qco_applicable": (
                True
                if compulsory is True
                else None
            ),
            "isi_mark_required": (
                True
                if compulsory is True
                else None
            ),
            "is_latest_version": (
                version.get("version_status") not in {
                    "Historical/Referenced",
                    "Historical / Referenced",
                }
                if version
                else None
            ),
            "recommended_standard": _standard_snapshot(
                primary
            ),
            "latest_amendment_year": (
                amendments.get("latest_amendment", {}).get(
                    "amendment_year"
                )
                if isinstance(
                    amendments.get("latest_amendment"),
                    dict
                )
                else None
            ),
            "recommendation": (
                certification.get("recommendation")
                or "Review certification and version intelligence."
            ),
        }

    return {
        "status": "Not available",
        "qco_applicable": None,
        "isi_mark_required": None,
        "is_latest_version": None,
        "recommended_standard": _standard_snapshot(
            primary
        ),
        "latest_amendment_year": None,
        "recommendation": (
            "Compliance intelligence was not returned. "
            "Ensure primary_standard is enriched before "
            "generating the procurement report."
        ),
    }


# ============================================================
# GAP ANALYSIS
# ============================================================

def _normalize_items(
    items: Any,
    default_severity: str,
    default_status: str,
) -> List[Dict]:
    """
    Defensive normalization for legacy Phase 5B responses.
    """
    if not isinstance(items, list):
        return []

    output: List[Dict] = []

    for item in items:
        if isinstance(item, dict):
            output.append(item)
        else:
            output.append({
                "requirement": str(item),
                "status": default_status,
                "severity": default_severity,
                "message": str(item),
            })

    return output


def _build_gaps_section(analysis: Dict) -> Dict:
    gap_analysis = (
        analysis.get("gap_analysis")
        or {}
    )

    gaps = _normalize_items(
        gap_analysis.get("gaps"),
        "HIGH",
        "GAP",
    )

    warnings = _normalize_items(
        gap_analysis.get("warnings"),
        "LOW",
        "WARNING",
    )

    verified = gap_analysis.get(
        "requirements_verified"
    ) or []

    if not isinstance(verified, list):
        verified = []

    # Highest-severity gaps first.
    gaps.sort(
        key=lambda item: _severity_rank(
            item.get("severity")
        ),
        reverse=True,
    )

    warnings.sort(
        key=lambda item: _severity_rank(
            item.get("severity")
        ),
        reverse=True,
    )

    source_summary = (
        gap_analysis.get("gap_summary")
        or {}
    )

    total_gaps = source_summary.get(
        "total_gaps",
        len(gaps),
    )

    high = source_summary.get(
        "high",
        sum(
            1 for item in gaps
            if item.get("severity") == "HIGH"
        ),
    )

    medium = source_summary.get(
        "medium",
        sum(
            1 for item in gaps
            if item.get("severity") == "MEDIUM"
        ),
    )

    low = source_summary.get(
        "low",
        sum(
            1 for item in gaps
            if item.get("severity") == "LOW"
        ),
    )

    total_warnings = source_summary.get(
        "total_warnings",
        len(warnings),
    )

    verified_count = source_summary.get(
        "verified_requirements",
        len(verified),
    )

    return {
        "summary": {
            "total_gaps": total_gaps,
            "high": high,
            "medium": medium,
            "low": low,
            "total_warnings": total_warnings,
            "verified_requirements": verified_count,
        },
        "items": gaps,
        "warnings": warnings,
        "verified_requirements": verified,
    }


# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

def _flatten_related_standards(
    related: Any
) -> List[Dict]:
    """
    Convert the knowledge graph response from its grouped form:

        {
            relationship_count: 18,
            category_counts: {...},
            test_references: [...],
            material_references: [...],
            conformity_inputs: [...],
            referenced_standards: [...]
        }

    into a flat list of actual relationship records.

    This prevents dictionary keys such as
    'relationship_count' and 'category_counts' from being
    incorrectly returned as fake standards.
    """

    if not related:
        return []

    if isinstance(related, list):
        return [
            item
            for item in related
            if isinstance(item, dict)
        ]

    if not isinstance(related, dict):
        return []

    output: List[Dict] = []

    categories = [
        "test_references",
        "material_references",
        "conformity_inputs",
        "referenced_standards",
    ]

    for category in categories:
        items = related.get(category) or []

        if not isinstance(items, list):
            continue

        for item in items:
            if not isinstance(item, dict):
                continue

            normalized = dict(item)

            normalized.setdefault(
                "category",
                category,
            )

            output.append(normalized)

    return output


def _build_related_standards(
    analysis: Dict
) -> Dict:
    related = (
        analysis.get("related_standards")
        or {}
    )

    if isinstance(related, list):
        return {
            "relationship_count": len(related),
            "category_counts": {},
            "standards": _flatten_related_standards(
                related
            ),
        }

    if not isinstance(related, dict):
        return {
            "relationship_count": 0,
            "category_counts": {},
            "standards": [],
        }

    return {
        "relationship_count": related.get(
            "relationship_count",
            0,
        ),
        "category_counts": related.get(
            "category_counts",
            {},
        ),
        "standards": _flatten_related_standards(
            related
        ),
    }


# ============================================================
# EVIDENCE
# ============================================================

def _build_evidence_section(
    analysis: Dict
) -> Dict:
    primary = (
        analysis.get("primary_standard")
        or {}
    )

    return {
        "source_authority": primary.get(
            "source_authority"
        ),
        "source_type": primary.get(
            "source_type"
        ),
        "source_document": primary.get(
            "source_document"
        ),
        "source_url": primary.get(
            "source_url"
        ),

        "explicit_standard_validation":
            analysis.get(
                "explicit_standard_validation",
                [],
            ),

        "version_resolution":
            primary.get(
                "version_intelligence"
            ),

        "amendment_intelligence":
            primary.get(
                "amendment_intelligence"
            ),

        "certification_intelligence":
            primary.get(
                "certification_intelligence"
            ),

        "analysis_scope":
            analysis.get(
                "analysis_scope",
                "Metadata-level procurement analysis; "
                "not clause-level compliance verification.",
            ),
    }


# ============================================================
# HUMAN REVIEW
# ============================================================

def _build_human_review_section(
    analysis: Dict
) -> Dict:
    return {
        "required": bool(
            analysis.get(
                "human_review_required"
            )
        ),
        "reasons": analysis.get(
            "review_reasons"
        ) or [],
    }


def _build_executive_status(
    analysis: Dict
) -> str:
    gap_analysis = (
        analysis.get("gap_analysis")
        or {}
    )

    summary = (
        gap_analysis.get("gap_summary")
        or {}
    )

    high = int(
        summary.get("high") or 0
    )

    total = int(
        summary.get("total_gaps") or 0
    )

    review_required = bool(
        analysis.get(
            "human_review_required"
        )
    )

    if high > 0:
        return "ACTION REQUIRED"

    if total > 0:
        return "REVIEW REQUIRED"

    if review_required:
        return "HUMAN REVIEW REQUIRED"

    return "READY FOR REVIEW"


# ============================================================
# RECOMMENDATIONS
# ============================================================

def _build_recommendations(
    analysis: Dict
) -> List[str]:
    gap_analysis = (
        analysis.get("gap_analysis")
        or {}
    )

    primary = (
        analysis.get("primary_standard")
        or {}
    )

    recommendations = gap_analysis.get(
        "recommendations"
    ) or []

    if not isinstance(
        recommendations,
        list,
    ):
        recommendations = []

    recommendations = [
        str(item)
        for item in recommendations
        if item
    ]

    if (
        not recommendations
        and primary.get("is_number")
    ):
        recommendations.append(
            f"Use {primary['is_number']} as the "
            "primary candidate standard, subject "
            "to human verification."
        )

    return recommendations


# ============================================================
# MAIN REPORT GENERATOR
# ============================================================

def generate_procurement_report(
    analysis: Dict
) -> Dict:
    """
    Convert the raw tender-analysis response into a
    judge-friendly Procurement Intelligence Report.

    This function is intentionally a reporting layer.
    It does not perform semantic search, version resolution,
    certification lookup, amendment lookup, or graph traversal.

    Those intelligence objects must already be present in
    primary_standard when tender_analysis_service.py calls
    this function.
    """

    if not isinstance(analysis, dict):
        raise TypeError(
            "analysis must be a dictionary returned by "
            "analyze_tender()."
        )

    primary = (
        analysis.get("primary_standard")
        or {}
    )

    requirements = (
        analysis.get("requirements_detected")
        or {}
    )

    gaps_section = _build_gaps_section(
        analysis
    )

    compliance = _build_compliance_section(
        analysis
    )

    related = _build_related_standards(
        analysis
    )

    recommendations = _build_recommendations(
        analysis
    )

    return {
        "report_type":
            "Procurement Intelligence Report",

        "report_version":
            "1.0",

        "executive_status":
            _build_executive_status(
                analysis
            ),

        "executive_summary": {
            "recommended_standard":
                _standard_snapshot(
                    primary
                ),

            "why_recommended":
                _build_why_recommended(
                    analysis
                ),

            "compliance_status":
                compliance.get(
                    "status"
                ),

            "gap_count":
                gaps_section[
                    "summary"
                ].get(
                    "total_gaps",
                    0,
                ),

            "high_severity_gaps":
                gaps_section[
                    "summary"
                ].get(
                    "high",
                    0,
                ),

            "human_review_required":
                bool(
                    analysis.get(
                        "human_review_required"
                    )
                ),
        },

        "tender_requirements":
            requirements,

        "recommended_standard":
            _standard_snapshot(
                primary
            ),

        "compliance":
            compliance,

        "gap_analysis":
            gaps_section,

        "applicable_standards":
            analysis.get(
                "applicable_standards",
                [],
            ),

        "related_standards":
            related,

        "evidence":
            _build_evidence_section(
                analysis
            ),

        "recommendations":
            recommendations,

        "human_review":
            _build_human_review_section(
                analysis
            ),

        "audit_trail":
            analysis.get(
                "audit_trail",
                [],
            ),
    }
