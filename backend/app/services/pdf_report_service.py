from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# =========================================================
# HELPERS
# =========================================================

def safe(value, default="Not available"):
    """
    Safely convert values to printable text.
    """
    if value is None or value == "":
        return default

    return str(value)


def yes_no(value):
    if value is True:
        return "YES"

    if value is False:
        return "NO"

    return "N/A"


def percentage(value):
    try:
        return f"{float(value) * 100:.2f}%"
    except (TypeError, ValueError):
        return "N/A"


def pretty(value):
    if not value:
        return "Not specified"

    return (
        str(value)
        .replace("_", " ")
        .title()
    )


# =========================================================
# PAGE HEADER / FOOTER
# =========================================================

def draw_header_footer(canvas, doc):

    canvas.saveState()

    width, height = A4

    # -----------------------------------------------------
    # Header
    # -----------------------------------------------------

    canvas.setStrokeColor(
        colors.HexColor("#D9E1EA")
    )

    canvas.line(
        18 * mm,
        height - 16 * mm,
        width - 18 * mm,
        height - 16 * mm,
    )

    canvas.setFont(
        "Helvetica-Bold",
        8
    )

    canvas.setFillColor(
        colors.HexColor("#173F78")
    )

    canvas.drawString(
        18 * mm,
        height - 12 * mm,
        "STANDARDSINSIGHT",
    )

    canvas.setFont(
        "Helvetica",
        7
    )

    canvas.setFillColor(
        colors.HexColor("#788696")
    )

    canvas.drawRightString(
        width - 18 * mm,
        height - 12 * mm,
        "Procurement Intelligence",
    )

    # -----------------------------------------------------
    # Footer
    # -----------------------------------------------------

    canvas.line(
        18 * mm,
        13 * mm,
        width - 18 * mm,
        13 * mm,
    )

    canvas.setFont(
        "Helvetica",
        6.5
    )

    canvas.setFillColor(
        colors.HexColor("#7A8795")
    )

    canvas.drawString(
        18 * mm,
        8 * mm,
        "AI-assisted analysis • Human verification enabled",
    )

    canvas.drawRightString(
        width - 18 * mm,
        8 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


# =========================================================
# SECTION TITLE
# =========================================================

def section_title(
    title,
    styles
):

    return Paragraph(
        title,
        styles["SectionTitle"]
    )


# =========================================================
# KEY-VALUE TABLE
# =========================================================

def key_value_table(
    rows,
    styles,
    column_widths=None
):

    data = []

    for label, value in rows:

        data.append(
            [
                Paragraph(
                    safe(label),
                    styles["TableLabel"]
                ),

                Paragraph(
                    safe(value),
                    styles["TableValue"]
                ),
            ]
        )

    table = Table(
        data,
        colWidths=(
            column_widths
            or [48 * mm, 122 * mm]
        ),
        repeatRows=0,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#F4F7FA"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#DCE3EA"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    return table


# =========================================================
# GENERATE PDF
# =========================================================

def generate_procurement_pdf(report: dict):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,

        rightMargin=18 * mm,
        leftMargin=18 * mm,

        topMargin=24 * mm,
        bottomMargin=19 * mm,

        title="StandardsInsight Procurement Intelligence Report",
        author="StandardsInsight",
    )

    # =====================================================
    # STYLES
    # =====================================================

    base_styles = getSampleStyleSheet()

    styles = {

        "Title": ParagraphStyle(
            "CustomTitle",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=27,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#173F78"),
            spaceAfter=6,
        ),

        "Subtitle": ParagraphStyle(
            "Subtitle",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#718096"),
            spaceAfter=18,
        ),

        "SectionTitle": ParagraphStyle(
            "SectionTitle",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#315F8E"),
            spaceBefore=10,
            spaceAfter=8,
        ),

        "Heading": ParagraphStyle(
            "Heading",
            parent=base_styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#293A52"),
            spaceAfter=6,
        ),

        "Body": ParagraphStyle(
            "Body",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=13,
            textColor=colors.HexColor("#58697D"),
            spaceAfter=6,
        ),

        "TableLabel": ParagraphStyle(
            "TableLabel",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#6B7B8D"),
        ),

        "TableValue": ParagraphStyle(
            "TableValue",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#34475E"),
        ),

        "StandardNumber": ParagraphStyle(
            "StandardNumber",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#173F78"),
            alignment=TA_CENTER,
            spaceAfter=5,
        ),

        "StandardTitle": ParagraphStyle(
            "StandardTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#45566C"),
            alignment=TA_CENTER,
            spaceAfter=12,
        ),

        "Small": ParagraphStyle(
            "Small",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=10,
            textColor=colors.HexColor("#748395"),
        ),

        "Bullet": ParagraphStyle(
            "Bullet",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=12,
            leftIndent=12,
            firstLineIndent=-7,
            textColor=colors.HexColor("#53657A"),
            spaceAfter=3,
        ),

    }

    story = []

    # =====================================================
    # REPORT HEADER
    # =====================================================

    story.append(
        Spacer(1, 10 * mm)
    )

    story.append(
        Paragraph(
            "STANDARDSINSIGHT",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "PROCUREMENT INTELLIGENCE REPORT",
            styles["Subtitle"]
        )
    )

    generated_at = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    story.append(
        key_value_table(
            [
                (
                    "Generated",
                    generated_at
                ),
                (
                    "Analysis Type",
                    "AI-Assisted Indian Standards Recommendation"
                ),
                (
                    "Verification Model",
                    "Human-in-the-Loop"
                ),
            ],
            styles
        )
    )

    story.append(
        Spacer(1, 8 * mm)
    )

    # =====================================================
    # EXECUTIVE STATUS
    # =====================================================

    story.append(
        section_title(
            "EXECUTIVE STATUS",
            styles
        )
    )

    executive_status = safe(
        report.get(
            "executive_status"
        ),
        "NOT AVAILABLE"
    )

    status_table = Table(
        [
            [
                Paragraph(
                    "Decision Status",
                    styles["TableLabel"]
                ),
                Paragraph(
                    executive_status,
                    styles["TableValue"]
                )
            ]
        ],
        colWidths=[
            48 * mm,
            122 * mm
        ]
    )

    status_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    colors.HexColor("#F4F7FA"),
                ),
                (
                    "BACKGROUND",
                    (1, 0),
                    (1, 0),
                    colors.HexColor("#FFF8E8")
                    if "REVIEW" in executive_status
                    else colors.HexColor("#EFF9F2"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.HexColor("#DCE3EA"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#DCE3EA"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(status_table)

    story.append(
        Spacer(1, 7 * mm)
    )

    # =====================================================
    # RECOMMENDED STANDARD
    # =====================================================

    story.append(
        section_title(
            "RECOMMENDED STANDARD",
            styles
        )
    )

    recommended = (
        report.get(
            "recommended_standard"
        )
        or {}
    )

    standard_number = safe(
        recommended.get(
            "is_number"
        )
    )

    standard_title = safe(
        recommended.get(
            "title"
        )
    )

    confidence = recommended.get(
        "confidence"
    )

    standard_box = Table(
        [
            [
                Paragraph(
                    standard_number,
                    styles["StandardNumber"]
                )
            ],
            [
                Paragraph(
                    standard_title,
                    styles["StandardTitle"]
                )
            ],
            [
                Paragraph(
                    f"Recommendation Confidence: "
                    f"<b>{percentage(confidence)}</b>",
                    styles["Body"]
                )
            ],
        ],
        colWidths=[170 * mm]
    )

    standard_box.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F7FAFD"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.HexColor("#CAD8E5"),
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
            ]
        )
    )

    story.append(standard_box)

    story.append(
        Spacer(1, 5 * mm)
    )

    # =====================================================
    # WHY RECOMMENDED
    # =====================================================

    why = report.get(
        "why_recommended"
    )

    if why:

        story.append(
            section_title(
                "WHY THIS STANDARD WAS RECOMMENDED",
                styles
            )
        )

        if isinstance(why, list):

            for item in why:

                story.append(
                    Paragraph(
                        f"• {safe(item)}",
                        styles["Bullet"]
                    )
                )

        else:

            story.append(
                Paragraph(
                    safe(why),
                    styles["Body"]
                )
            )

    # =====================================================
    # TENDER REQUIREMENTS
    # =====================================================

    requirements = (
        report.get(
            "tender_requirements"
        )
        or {}
    )

    story.append(
        section_title(
            "REQUIREMENT EXTRACTION",
            styles
        )
    )

    requirement_rows = [
        (
            "Product",
            requirements.get("product")
        ),
        (
            "Material",
            requirements.get("material")
        ),
        (
            "Cement Type",
            requirements.get("cement_type")
        ),
        (
            "Grade",
            requirements.get("grade")
        ),
        (
            "Application",
            requirements.get("application")
        ),
        (
            "Certification Required",
            yes_no(
                requirements.get(
                    "certification_required"
                )
            ),
        ),
    ]

    story.append(
        key_value_table(
            requirement_rows,
            styles
        )
    )

    # =====================================================
    # COMPLIANCE
    # =====================================================

    compliance = (
        report.get(
            "compliance"
        )
        or {}
    )

    story.append(
        section_title(
            "COMPLIANCE INTELLIGENCE",
            styles
        )
    )

    compliance_rows = [
        (
            "Overall Status",
            compliance.get("status")
        ),
        (
            "QCO Applicable",
            yes_no(
                compliance.get(
                    "qco_applicable"
                )
            ),
        ),
        (
            "ISI Mark Required",
            yes_no(
                compliance.get(
                    "isi_mark_required"
                )
            ),
        ),
        (
            "Latest Version",
            yes_no(
                compliance.get(
                    "is_latest_version"
                )
            ),
        ),
        (
            "Latest Amendment",
            compliance.get(
                "latest_amendment_year"
            ),
        ),
    ]

    story.append(
        key_value_table(
            compliance_rows,
            styles
        )
    )

    # =====================================================
    # GAP ANALYSIS
    # =====================================================

    gap_analysis = (
        report.get(
            "gap_analysis"
        )
        or {}
    )

    summary = (
        gap_analysis.get(
            "summary"
        )
        or {}
    )

    story.append(
        section_title(
            "PROCUREMENT GAP ANALYSIS",
            styles
        )
    )

    gap_summary_rows = [
        (
            "Total Gaps",
            summary.get(
                "total_gaps",
                0
            ),
        ),
        (
            "High Severity",
            summary.get(
                "high",
                0
            ),
        ),
        (
            "Medium Severity",
            summary.get(
                "medium",
                0
            ),
        ),
        (
            "Low Severity",
            summary.get(
                "low",
                0
            ),
        ),
    ]

    story.append(
        key_value_table(
            gap_summary_rows,
            styles
        )
    )

    gaps = gap_analysis.get(
        "items"
    ) or []

    if gaps:

        story.append(
            Spacer(1, 3 * mm)
        )

        for gap in gaps:

            severity = safe(
                gap.get(
                    "severity"
                ),
                "MEDIUM"
            )

            requirement = safe(
                gap.get(
                    "requirement"
                ),
                "Requirement"
            )

            message = safe(
                gap.get(
                    "message"
                ),
                "Verification required."
            )

            action = gap.get(
                "recommended_action"
            )

            story.append(
                Paragraph(
                    f"<b>{severity}</b> — "
                    f"{requirement}: "
                    f"{message}",
                    styles["Bullet"]
                )
            )

            if action:

                story.append(
                    Paragraph(
                        f"Recommended action: "
                        f"{safe(action)}",
                        styles["Small"]
                    )
                )

    else:

        story.append(
            Spacer(1, 3 * mm)
        )

        story.append(
            Paragraph(
                "✓ No procurement gaps detected "
                "by the current verified intelligence.",
                styles["Body"]
            )
        )

    # =====================================================
    # RELATED STANDARDS
    # =====================================================

    related = (
        report.get(
            "related_standards"
        )
        or {}
    )

    story.append(
        section_title(
            "KNOWLEDGE GRAPH — RELATED STANDARDS",
            styles
        )
    )

    category_counts = (
        related.get(
            "category_counts"
        )
        or {}
    )

    related_summary = [
        (
            "Total Relationships",
            related.get(
                "relationship_count",
                0
            ),
        ),
        (
            "Test References",
            category_counts.get(
                "test_references",
                0
            ),
        ),
        (
            "Material References",
            category_counts.get(
                "material_references",
                0
            ),
        ),
        (
            "Conformity Inputs",
            category_counts.get(
                "conformity_inputs",
                0
            ),
        ),
    ]

    story.append(
        key_value_table(
            related_summary,
            styles
        )
    )

    related_standards = (
        related.get(
            "standards"
        )
        or []
    )

    if related_standards:

        story.append(
            Spacer(1, 3 * mm)
        )

        relation_rows = [
            [
                Paragraph(
                    "Standard",
                    styles["TableLabel"]
                ),
                Paragraph(
                    "Relationship",
                    styles["TableLabel"]
                ),
            ]
        ]

        for item in related_standards:

            relation_rows.append(
                [
                    Paragraph(
                        safe(
                            item.get(
                                "is_number",
                                item.get(
                                    "standard_number",
                                    item.get(
                                        "reference"
                                    )
                                )
                            )
                        ),
                        styles["TableValue"]
                    ),
                    Paragraph(
                        pretty(
                            item.get(
                                "relationship_type"
                            )
                        ),
                        styles["TableValue"]
                    ),
                ]
            )

        relation_table = Table(
            relation_rows,
            colWidths=[
                65 * mm,
                105 * mm
            ]
        )

        relation_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#F0F4F8"),
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#DCE3EA"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(
            relation_table
        )

    # =====================================================
    # EVIDENCE
    # =====================================================

    evidence = (
        report.get(
            "evidence"
        )
        or {}
    )

    story.append(
        section_title(
            "EVIDENCE & SOURCE",
            styles
        )
    )

    evidence_rows = [
        (
            "Source Authority",
            evidence.get(
                "source_authority"
            ),
        ),
        (
            "Source Type",
            evidence.get(
                "source_type"
            ),
        ),
        (
            "Verification Status",
            evidence.get(
                "verification_status"
            ),
        ),
        (
            "Source Document",
            evidence.get(
                "source_document"
            ),
        ),
        (
            "Source URL",
            evidence.get(
                "source_url"
            ),
        ),
    ]

    story.append(
        key_value_table(
            evidence_rows,
            styles
        )
    )

    # =====================================================
    # HUMAN REVIEW
    # =====================================================

    human_review = (
        report.get(
            "human_review"
        )
        or {}
    )

    story.append(
        section_title(
            "HUMAN REVIEW",
            styles
        )
    )

    review_required = human_review.get(
        "required"
    )

    story.append(
        key_value_table(
            [
                (
                    "Review Required",
                    yes_no(
                        review_required
                    ),
                ),
            ],
            styles
        )
    )

    reasons = human_review.get(
        "reasons"
    ) or []

    if reasons:

        story.append(
            Spacer(1, 3 * mm)
        )

        for reason in reasons:

            story.append(
                Paragraph(
                    f"• {safe(reason)}",
                    styles["Bullet"]
                )
            )

    # =====================================================
    # AUDIT TRAIL
    # =====================================================

    audit_trail = (
        report.get(
            "audit_trail"
        )
        or []
    )

    if audit_trail:

        story.append(
            PageBreak()
        )

        story.append(
            section_title(
                "AUDIT TRAIL",
                styles
            )
        )

        for index, step in enumerate(
            audit_trail,
            start=1
        ):

            story.append(
                Paragraph(
                    f"<b>{index}.</b> "
                    f"{pretty(step)}",
                    styles["Bullet"]
                )
            )

    # =====================================================
    # FINAL DISCLAIMER
    # =====================================================

    story.append(
        Spacer(1, 10 * mm)
    )

    disclaimer = Table(
        [
            [
                Paragraph(
                    "<b>IMPORTANT:</b> "
                    "This report provides AI-assisted "
                    "procurement intelligence based on "
                    "the available verified dataset. "
                    "Final procurement and compliance "
                    "decisions should be validated by "
                    "an authorized human reviewer and "
                    "the applicable official BIS sources.",
                    styles["Small"]
                )
            ]
        ],
        colWidths=[170 * mm]
    )

    disclaimer.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#FFF9EA"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#E8D8A9"),
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(
        disclaimer
    )

    # =====================================================
    # BUILD
    # =====================================================

    document.build(
        story,
        onFirstPage=draw_header_footer,
        onLaterPages=draw_header_footer,
    )

    buffer.seek(0)

    return buffer