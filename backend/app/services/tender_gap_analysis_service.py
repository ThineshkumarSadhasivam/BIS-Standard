from typing import Dict, List


# ============================================================
# SEVERITY ORDER
# ============================================================

SEVERITY_ORDER = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}


# ============================================================
# GAP CREATOR
# ============================================================

def create_gap(
    requirement: str,
    message: str,
    severity: str,
    evidence=None,
    action: str = "",
) -> Dict:

    return {
        "requirement": requirement,
        "severity": severity,
        "status": "GAP",
        "message": message,
        "evidence": evidence or {},
        "recommended_action": action,
    }


# ============================================================
# WARNING CREATOR
# ============================================================

def create_warning(
    warning_type: str,
    message: str,
    severity: str,
    evidence=None,
    action: str = "",
) -> Dict:

    return {
        "type": warning_type,
        "severity": severity,
        "message": message,
        "evidence": evidence or {},
        "recommended_action": action,
    }


# ============================================================
# VERIFIED REQUIREMENT
# ============================================================

def create_verified(
    requirement: str,
    value=None,
    evidence=None,
) -> Dict:

    result = {
        "requirement": requirement,
        "status": "SATISFIED",
    }

    if value is not None:
        result["value"] = value

    if evidence:
        result["evidence"] = evidence

    return result


# ============================================================
# GAP ANALYSIS
# ============================================================

def analyze_tender_gaps(
    requirements: Dict,
    primary_standard: Dict,
    existing_gaps: List[Dict],
    explicit_reference_validation: List[Dict],
) -> Dict:

    gaps = []
    warnings = []
    verified = []
    recommendations = []

    # --------------------------------------------------------
    # Product
    # --------------------------------------------------------

    product = requirements.get(
        "product"
    )

    if product:

        verified.append(
            create_verified(
                requirement="Product",
                value=product,
                evidence={
                    "source": "Tender text"
                },
            )
        )

    else:

        gaps.append(
            create_gap(
                requirement="Product identification",
                message=(
                    "The tender does not clearly "
                    "identify the procurement product."
                ),
                severity="HIGH",
                action=(
                    "Specify the exact product or material "
                    "being procured."
                ),
            )
        )

    # --------------------------------------------------------
    # Material
    # --------------------------------------------------------

    material = requirements.get(
        "material"
    )

    if material:

        verified.append(
            create_verified(
                requirement="Material",
                value=material,
                evidence={
                    "source": "Tender text"
                },
            )
        )

    # --------------------------------------------------------
    # Cement type
    # --------------------------------------------------------

    cement_type = requirements.get(
        "cement_type"
    )

    if product == "cement":

        if cement_type:

            verified.append(
                create_verified(
                    requirement="Cement type",
                    value=cement_type,
                    evidence={
                        "source": "Tender text"
                    },
                )
            )

        else:

            gaps.append(
                create_gap(
                    requirement="Cement type",
                    message=(
                        "The tender identifies cement "
                        "but does not specify the cement type."
                    ),
                    severity="MEDIUM",
                    action=(
                        "Specify the applicable cement type "
                        "before procurement."
                    ),
                )
            )

    # --------------------------------------------------------
    # Cement grade
    # --------------------------------------------------------

    grade = requirements.get(
        "grade"
    )

    if product == "cement":

        if grade:

            verified.append(
                create_verified(
                    requirement="Cement grade",
                    value=grade,
                    evidence={
                        "source": "Tender text"
                    },
                )
            )

        else:

            gaps.append(
                create_gap(
                    requirement="Cement grade",
                    message=(
                        "Cement grade is not explicitly "
                        "specified in the tender."
                    ),
                    severity="MEDIUM",
                    action=(
                        "Specify the required cement grade "
                        "such as 33, 43 or 53, subject to "
                        "project requirements."
                    ),
                )
            )

    # --------------------------------------------------------
    # Application
    # --------------------------------------------------------

    application = requirements.get(
        "application"
    )

    if application:

        verified.append(
            create_verified(
                requirement="Application",
                value=application,
                evidence={
                    "source": "Tender text"
                },
            )
        )

    else:

        warnings.append(
            create_warning(
                warning_type="APPLICATION_NOT_SPECIFIED",
                message=(
                    "The intended application was not "
                    "clearly extracted from the tender."
                ),
                severity="LOW",
                action=(
                    "Specify the intended application or "
                    "project use where relevant."
                ),
            )
        )

    # --------------------------------------------------------
    # Certification
    # --------------------------------------------------------

    certification_required = requirements.get(
        "certification_required",
        False
    )

    certification_gap = next(
        (
            gap
            for gap in existing_gaps
            if gap.get(
                "requirement"
            ) == "BIS certification"
        ),
        None,
    )

    if certification_gap:

        if certification_gap.get(
            "status"
        ) == "FOUND":

            verified.append(
                create_verified(
                    requirement="BIS certification",
                    value="Explicitly required",
                    evidence=(
                        certification_gap.get(
                            "evidence"
                        )
                    ),
                )
            )

        elif certification_gap.get(
            "status"
        ) == "GAP":

            gaps.append(
                create_gap(
                    requirement="BIS certification",
                    message=(
                        certification_gap.get(
                            "message"
                        )
                    ),
                    severity="HIGH",
                    evidence=(
                        certification_gap.get(
                            "evidence"
                        )
                    ),
                    action=(
                        "Explicitly include the applicable "
                        "BIS certification requirement and "
                        "verify the relevant QCO/certification "
                        "conditions."
                    ),
                )
            )

        elif certification_gap.get(
            "status"
        ) == "REVIEW":

            warnings.append(
                create_warning(
                    warning_type="CERTIFICATION_REVIEW",
                    message=(
                        certification_gap.get(
                            "message"
                        )
                    ),
                    severity="MEDIUM",
                    evidence=(
                        certification_gap.get(
                            "evidence"
                        )
                    ),
                    action=(
                        "Manually verify the applicable "
                        "BIS certification requirement."
                    ),
                )
            )

    # --------------------------------------------------------
    # Version
    # --------------------------------------------------------

    version_gap = next(
        (
            gap
            for gap in existing_gaps
            if gap.get(
                "requirement"
            ) == "Current standard version"
        ),
        None,
    )

    if version_gap:

        if version_gap.get(
            "status"
        ) == "OK":

            verified.append(
                create_verified(
                    requirement="Current standard version",
                    value=primary_standard.get(
                        "is_number"
                    ),
                    evidence=(
                        version_gap.get(
                            "evidence"
                        )
                    ),
                )
            )

        elif version_gap.get(
            "status"
        ) == "GAP":

            gaps.append(
                create_gap(
                    requirement="Current standard version",
                    message=(
                        version_gap.get(
                            "message"
                        )
                    ),
                    severity="HIGH",
                    evidence=(
                        version_gap.get(
                            "evidence"
                        )
                    ),
                    action=(
                        "Replace the historical standard "
                        "reference with the applicable current "
                        "standard after human verification."
                    ),
                )
            )

    # --------------------------------------------------------
    # Explicit standard references
    # --------------------------------------------------------

    for reference in explicit_reference_validation:

        if reference.get(
            "status"
        ) == "FOUND":

            version_info = reference.get(
                "version_intelligence"
            ) or {}

            version_status = (
                version_info.get(
                    "version_status"
                )
                or ""
            ).lower()

            if (
                "historical" in version_status
                or "referenced" in version_status
            ):

                gaps.append(
                    create_gap(
                        requirement=(
                            f"Referenced standard "
                            f"{reference.get('reference')}"
                        ),
                        message=(
                            f"{reference.get('reference')} "
                            "is identified as a historical/"
                            "referenced version."
                        ),
                        severity="HIGH",
                        evidence=version_info,
                        action=(
                            "Verify the current applicable "
                            "BIS standard before finalizing "
                            "the procurement specification."
                        ),
                    )
                )

            else:

                verified.append(
                    create_verified(
                        requirement=(
                            "Explicit standard reference"
                        ),
                        value=reference.get(
                            "reference"
                        ),
                        evidence=version_info,
                    )
                )

        elif reference.get(
            "status"
        ) == "NOT_FOUND":

            gaps.append(
                create_gap(
                    requirement=(
                        f"Referenced standard "
                        f"{reference.get('reference')}"
                    ),
                    message=(
                        "The explicitly referenced standard "
                        "could not be resolved in the current "
                        "verified dataset."
                    ),
                    severity="HIGH",
                    evidence=reference,
                    action=(
                        "Manually verify the standard number "
                        "and its applicability."
                    ),
                )
            )

    # --------------------------------------------------------
    # Existing amendment review
    # --------------------------------------------------------

    amendment_gap = next(
        (
            gap
            for gap in existing_gaps
            if gap.get(
                "requirement"
            ) == "Amendment awareness"
        ),
        None,
    )

    if amendment_gap:

        if amendment_gap.get(
            "status"
        ) == "REVIEW":

            warnings.append(
                create_warning(
                    warning_type="AMENDMENT_REVIEW",
                    message=(
                        amendment_gap.get(
                            "message"
                        )
                    ),
                    severity="MEDIUM",
                    evidence=(
                        amendment_gap.get(
                            "evidence"
                        )
                    ),
                    action=(
                        "Review the recorded amendments "
                        "and ensure the applicable version "
                        "and amendments are reflected in "
                        "the procurement specification."
                    ),
                )
            )

        elif amendment_gap.get(
            "status"
        ) == "NO_EVIDENCE":

            amendment_evidence = (
                amendment_gap.get("evidence") or {}
            )

            warnings.append(
                create_warning(
                    warning_type="AMENDMENT_NO_DATA",
                    message=(
                        "No amendment records are currently "
                        "available for this standard in the "
                        "verified dataset."
                    ),
                    severity="LOW",
                    evidence=amendment_evidence,
                    action=(
                        "Verify the latest BIS standard record "
                        "and applicable amendments before finalizing "
                        "the procurement specification."
                    ),
                )
            )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    confidence = float(
        primary_standard.get(
            "confidence",
            0.0
        )
    )

    if confidence < 0.60:

        warnings.append(
            create_warning(
                warning_type="LOW_RECOMMENDATION_CONFIDENCE",
                message=(
                    f"The primary standard recommendation "
                    f"has a confidence score of "
                    f"{confidence:.2f}, below the 0.60 "
                    "human-review threshold."
                ),
                severity="HIGH",
                evidence={
                    "confidence":
                        confidence,
                    "standard":
                        primary_standard.get(
                            "is_number"
                        ),
                },
                action=(
                    "Have a procurement/standards expert "
                    "verify the recommended standard."
                ),
            )
        )

    # --------------------------------------------------------
    # General recommendation
    # --------------------------------------------------------

    if primary_standard:

        recommendations.append(
            (
                f"Use {primary_standard.get('is_number')} "
                "as the primary candidate standard, "
                "subject to human verification."
            )
        )

    if certification_required:

        recommendations.append(
            "Retain the certification requirement in "
            "the final procurement specification."
        )

    # --------------------------------------------------------
    # Sort by severity
    # --------------------------------------------------------

    gaps.sort(
        key=lambda item: SEVERITY_ORDER.get(
            item.get("severity"),
            0
        ),
        reverse=True,
    )

    warnings.sort(
        key=lambda item: SEVERITY_ORDER.get(
            item.get("severity"),
            0
        ),
        reverse=True,
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    high_gaps = sum(
        1
        for gap in gaps
        if gap.get("severity") == "HIGH"
    )

    medium_gaps = sum(
        1
        for gap in gaps
        if gap.get("severity") == "MEDIUM"
    )

    low_gaps = sum(
        1
        for gap in gaps
        if gap.get("severity") == "LOW"
    )

    return {
        "gap_summary": {
            "total_gaps":
                len(gaps),

            "high":
                high_gaps,

            "medium":
                medium_gaps,

            "low":
                low_gaps,

            "total_warnings":
                len(warnings),

            "verified_requirements":
                len(verified),
        },

        "requirements_verified":
            verified,

        "gaps":
            gaps,

        "warnings":
            warnings,

        "recommendations":
            recommendations,
    }
