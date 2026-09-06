import re
from typing import List, Dict


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

]


# =========================================================
# TOKENIZATION
# =========================================================

def tokenize(
    text: str
) -> List[str]:

    if not text:
        return []

    text = text.lower()

    tokens = re.findall(
        r"[a-z0-9]+",
        text
    )

    return [
        token
        for token in tokens
        if token not in STOP_WORDS
    ]


# =========================================================
# TITLE MATCHING
# =========================================================

def lexical_title_score(
    query: str,
    title: str
) -> float:

    query_tokens = set(
        tokenize(query)
    )

    title_tokens = set(
        tokenize(title)
    )

    if (
        not query_tokens
        or not title_tokens
    ):
        return 0.0

    overlap = (
        query_tokens
        .intersection(title_tokens)
    )

    return (
        len(overlap)
        /
        len(query_tokens)
    )


# =========================================================
# PHRASE MATCHING
# =========================================================

def phrase_match_score(
    query: str,
    title: str
) -> float:

    if (
        not query
        or not title
    ):
        return 0.0

    query_lower = query.lower()
    title_lower = title.lower()

    matches = 0

    for phrase in IMPORTANT_PHRASES:

        if (
            phrase in query_lower
            and phrase in title_lower
        ):

            matches += 1

    if matches == 0:
        return 0.0

    return min(
        matches * 0.5,
        1.0
    )


# =========================================================
# DOMAIN MATCHING
# =========================================================

def domain_score(
    query: str,
    domain: str
) -> float:

    query_tokens = set(
        tokenize(query)
    )

    domain_tokens = set(
        tokenize(domain)
    )

    if (
        not query_tokens
        or not domain_tokens
    ):
        return 0.0

    overlap = (
        query_tokens
        .intersection(domain_tokens)
    )

    return min(
        len(overlap)
        /
        len(query_tokens),
        1.0
    )


# =========================================================
# STANDARD TYPE MATCHING
# =========================================================

def standard_type_score(
    query: str,
    standard_type: str
) -> float:

    query_lower = query.lower()

    standard_type_lower = (
        standard_type or ""
    ).lower()

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

def status_score(
    status: str
) -> float:

    status_lower = (
        status or ""
    ).lower()

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
# ATTRIBUTE MATCHING
# =========================================================

def attribute_match_score(
    query_intent,
    result: Dict
) -> float:

    """
    Compare structured procurement intent against
    a retrieved Indian Standard.

    Scoring philosophy:

        Strong positive
            Explicitly matches requested attribute.

        Small positive
            Broad/general compatibility.

        Negative
            Specialized or conflicting candidate.

    The function intentionally avoids treating generic
    words such as "cement", "concrete", or "structural"
    as sufficient evidence for primary relevance.
    """

    title = (
        result.get("title", "")
        or ""
    ).lower()

    domain = (
        result.get("domain", "")
        or ""
    ).lower()

    standard_type = (
        result.get("standard_type", "")
        or ""
    ).lower()

    score = 0.0

    # =====================================================
    # QUERY ATTRIBUTES
    # =====================================================

    product = getattr(
        query_intent,
        "product",
        None
    )

    cement_type = getattr(
        query_intent,
        "cement_type",
        None
    )

    requested_grade = getattr(
        query_intent,
        "grade",
        None
    )

    application = getattr(
        query_intent,
        "application",
        None
    )

    structural_use = getattr(
        query_intent,
        "structural_use",
        False
    )

    seismic_requirement = getattr(
        query_intent,
        "seismic_requirement",
        False
    )

    requested_standard_type = getattr(
        query_intent,
        "standard_type",
        None
    )

    # =====================================================
    # PRODUCT MATCH
    # =====================================================

    if product == "cement":

    # Candidate must at least be about cement.
        if "cement" in title or "cement" in domain:
            score += 0.75
        else:
            score -= 2.0

    # -------------------------------------------------
    # SPECIALIZED CEMENT TYPES
    # -------------------------------------------------

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

    requested_specialization = False

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
            []
        )

        requested_specialization = any(
            keyword in title
            for keyword in requested_keywords
        )

        if requested_specialization:
            score += 2.0
        else:
            # A different/specialized cement type was found
            # but the requested type does not match.
            score -= 1.0

    # -------------------------------------------------
    # GENERIC CEMENT QUERY
    # -------------------------------------------------
    # If the user only says "cement" without specifying
    # the cement type, specialized cement standards should
    # not outrank a general cement standard merely because
    # they contain words such as "structural use".

    if not cement_type:

        has_specialized_cement = any(
            term in title
            for term in specialized_terms
        )

        if has_specialized_cement:
            score -= 1.5

        # Give a small preference to general Ordinary
        # Portland Cement when the query is generic.
        if "ordinary portland cement" in title:
            score += 1.0

    # -------------------------------------------------
    # EXPLICIT ORDINARY PORTLAND CEMENT
    # -------------------------------------------------
    # If the user explicitly asks for OPC, strongly favor
    # OPC standards and suppress other specialized types.

    if (
        cement_type
        == "ordinary portland cement"
    ):

        if (
            "ordinary portland cement"
            in title
        ):
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

        # A concrete query should not automatically
        # promote reinforcement steel standards.

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
    # GRADE MATCH
    # =====================================================

    if requested_grade:

        requested_grade_pattern = (
            rf"\b{requested_grade}\s*grade\b"
        )

        # Exact requested grade.
        if re.search(
            requested_grade_pattern,
            title
        ):

            score += 3.0

        # Explicitly different grade.
        other_grades = {
            "33",
            "43",
            "53",
        } - {
            requested_grade
        }

        for grade in other_grades:

            if re.search(
                rf"\b{grade}\s*grade\b",
                title
            ):

                score -= 3.0

                break

    # =====================================================
    # APPLICATION
    # =====================================================

    if application:

        # -------------------------------------------------
        # PLAIN + REINFORCED CONCRETE
        # -------------------------------------------------

        if (
            application
            == "plain and reinforced concrete"
        ):

            if (
                "plain and reinforced concrete"
                in title
            ):

                score += 2.5

            elif (
                "reinforced concrete"
                in title
                and "plain" in title
            ):

                score += 1.5

        # -------------------------------------------------
        # REINFORCED CONCRETE
        # -------------------------------------------------

        elif (
            application
            == "reinforced concrete"
        ):

            if (
                "reinforced concrete"
                in title
            ):

                score += 1.25

            elif "concrete" in title:

                score += 0.25

        # -------------------------------------------------
        # PLAIN CONCRETE
        # -------------------------------------------------

        elif (
            application
            == "plain concrete"
        ):

            if "plain concrete" in title:

                score += 1.5

        # -------------------------------------------------
        # STRUCTURAL CONCRETE
        # -------------------------------------------------

        elif (
            application
            == "structural concrete"
        ):

            if (
                "structural concrete"
                in title
            ):

                score += 1.5

            elif "concrete" in title:

                score += 0.25

        # -------------------------------------------------
        # BUILDING CONSTRUCTION
        # -------------------------------------------------

        elif (
            application
            == "building construction"
        ):

            if (
                "building" in title
                or "construction" in title
            ):

                score += 0.5

    # =====================================================
    # STRUCTURAL USE
    # =====================================================

    if structural_use:

        # Structural wording is supporting evidence,
        # not a primary product match.

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
    # STANDARD TYPE
    # =====================================================

    if requested_standard_type:

        if (
            requested_standard_type
            == "specification"
        ):

            if "specification" in standard_type:

                score += 0.75

        elif (
            requested_standard_type
            == "code_of_practice"
        ):

            if "code of practice" in standard_type:

                score += 0.75

        elif (
            requested_standard_type
            == "test_method"
        ):

            if "test" in standard_type:

                score += 0.75

        elif (
            requested_standard_type
            == "guideline"
        ):

            if "guideline" in standard_type:

                score += 0.75

    # =====================================================
    # TEST METHODS
    # =====================================================

    # Test methods are generally supporting/related
    # standards, not primary product specifications,
    # unless the query explicitly asks for testing.

    if (
        "test" in standard_type
        and requested_standard_type
        != "test_method"
    ):

        score -= 0.5

    return score


# =========================================================
# FINAL SCORE
# =========================================================

def calculate_final_score(
    query: str,
    result: Dict,
    query_intent=None
) -> Dict:

    # =====================================================
    # SEMANTIC
    # =====================================================

    semantic_score = float(
        result.get(
            "score",
            0.0
        )
    )

    # =====================================================
    # TITLE
    # =====================================================

    title_score = lexical_title_score(
        query,
        result.get(
            "title",
            ""
        )
    )

    # =====================================================
    # DOMAIN
    # =====================================================

    domain_match = domain_score(
        query,
        result.get(
            "domain",
            ""
        )
    )

    # =====================================================
    # STANDARD TYPE
    # =====================================================

    type_match = standard_type_score(
        query,
        result.get(
            "standard_type",
            ""
        )
    )

    # =====================================================
    # PHRASE
    # =====================================================

    phrase_match = phrase_match_score(
        query,
        result.get(
            "title",
            ""
        )
    )

    # =====================================================
    # STATUS
    # =====================================================

    status_match = status_score(
        result.get(
            "status",
            ""
        )
    )

    # =====================================================
    # ATTRIBUTE
    # =====================================================

    if query_intent is not None:

        attribute_score = attribute_match_score(
            query_intent,
            result
        )

        attribute_score_normalized = max(
            -1.0,
            min(
                attribute_score / 4.0,
                1.0
            )
        )

    else:

        attribute_score = 0.0

        attribute_score_normalized = 0.0

    # =====================================================
    # FINAL HYBRID SCORE
    # =====================================================

    final_score = (

        SEMANTIC_WEIGHT
        * semantic_score

        + TITLE_WEIGHT
        * title_score

        + DOMAIN_WEIGHT
        * domain_match

        + TYPE_WEIGHT
        * type_match

        + PHRASE_WEIGHT
        * phrase_match

        + STATUS_WEIGHT
        * status_match

        + ATTRIBUTE_WEIGHT
        * attribute_score_normalized
    )

    # =====================================================
    # COPY RESULT
    # =====================================================

    result = result.copy()

    result["semantic_score"] = round(
        semantic_score,
        4
    )

    result["title_score"] = round(
        title_score,
        4
    )

    result["domain_score"] = round(
        domain_match,
        4
    )

    result["type_score"] = round(
        type_match,
        4
    )

    result["phrase_score"] = round(
        phrase_match,
        4
    )

    result["status_score"] = round(
        status_match,
        4
    )

    result["attribute_score"] = round(
        attribute_score,
        4
    )

    result["final_score"] = round(
        final_score,
        4
    )

    return result


# =========================================================
# RERANK
# =========================================================

def rerank_results(
    query: str,
    results: List[Dict],
    query_intent=None
) -> List[Dict]:

    reranked = [

        calculate_final_score(
            query=query,
            result=result,
            query_intent=query_intent
        )

        for result in results
    ]

    # =====================================================
    # SORT
    # =====================================================

    reranked.sort(
        key=lambda item: item["final_score"],
        reverse=True
    )

    # =====================================================
    # REASSIGN RANK
    # =====================================================

    for rank, result in enumerate(
        reranked,
        start=1
    ):

        result["rank"] = rank

    return reranked