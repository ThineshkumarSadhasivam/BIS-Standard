import re
from typing import List, Dict


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


# ---------------------------------------------------------
# RERANKING WEIGHTS
# ---------------------------------------------------------

SEMANTIC_WEIGHT = 0.55
TITLE_WEIGHT = 0.20
DOMAIN_WEIGHT = 0.10
TYPE_WEIGHT = 0.05
PHRASE_WEIGHT = 0.10
STATUS_WEIGHT = 0.05


# ---------------------------------------------------------
# IMPORTANT PHRASES
# ---------------------------------------------------------

IMPORTANT_PHRASES = [
    "reinforced concrete",
    "plain and reinforced concrete",
    "ordinary portland cement",
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


# ---------------------------------------------------------
# TOKENIZATION
# ---------------------------------------------------------

def tokenize(text: str) -> List[str]:

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


# ---------------------------------------------------------
# TITLE MATCHING
# ---------------------------------------------------------

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

    if not query_tokens or not title_tokens:
        return 0.0

    overlap = query_tokens.intersection(
        title_tokens
    )

    return len(overlap) / len(query_tokens)


# ---------------------------------------------------------
# PHRASE MATCHING
# ---------------------------------------------------------

def phrase_match_score(
    query: str,
    title: str
) -> float:

    if not query or not title:
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

    # One matching phrase = 0.5
    # Two matching phrases = 1.0
    return min(
        matches * 0.5,
        1.0
    )


# ---------------------------------------------------------
# DOMAIN MATCHING
# ---------------------------------------------------------

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

    if not query_tokens or not domain_tokens:
        return 0.0

    overlap = query_tokens.intersection(
        domain_tokens
    )

    return min(
        len(overlap) / len(query_tokens),
        1.0
    )


# ---------------------------------------------------------
# STANDARD TYPE MATCHING
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# STATUS MATCHING
# ---------------------------------------------------------

def status_score(
    status: str
) -> float:

    status_lower = (
        status or ""
    ).lower()

    # Current standards receive a positive signal
    if "active/current" in status_lower:
        return 1.0

    # Historical standards receive a negative signal
    if "historical" in status_lower:
        return -1.0

    # Referenced standards get a smaller penalty
    if "referenced" in status_lower:
        return -0.5

    return 0.0


# ---------------------------------------------------------
# FINAL SCORE
# ---------------------------------------------------------

def calculate_final_score(
    query: str,
    result: Dict
) -> Dict:

    semantic_score = float(
        result.get("score", 0.0)
    )

    title_score = lexical_title_score(
        query,
        result.get("title", "")
    )

    domain_match = domain_score(
        query,
        result.get("domain", "")
    )

    type_match = standard_type_score(
        query,
        result.get("standard_type", "")
    )

    phrase_match = phrase_match_score(
        query,
        result.get("title", "")
    )

    status_match = status_score(
        result.get("status", "")
    )

    # -----------------------------------------------------
    # HYBRID RANKING SCORE
    # -----------------------------------------------------

    final_score = (
        SEMANTIC_WEIGHT * semantic_score
        + TITLE_WEIGHT * title_score
        + DOMAIN_WEIGHT * domain_match
        + TYPE_WEIGHT * type_match
        + PHRASE_WEIGHT * phrase_match
        + STATUS_WEIGHT * status_match
    )

    result = result.copy()

    # Original semantic similarity
    result["semantic_score"] = round(
        semantic_score,
        4
    )

    # Token-based title similarity
    result["title_score"] = round(
        title_score,
        4
    )

    # Domain similarity
    result["domain_score"] = round(
        domain_match,
        4
    )

    # Standard type similarity
    result["type_score"] = round(
        type_match,
        4
    )

    # Important phrase matching
    result["phrase_score"] = round(
        phrase_match,
        4
    )

    # Current / historical status
    result["status_score"] = round(
        status_match,
        4
    )

    # Final hybrid score
    result["final_score"] = round(
        final_score,
        4
    )

    return result


# ---------------------------------------------------------
# RERANK
# ---------------------------------------------------------

def rerank_results(
    query: str,
    results: List[Dict]
) -> List[Dict]:

    reranked = [
        calculate_final_score(
            query,
            result
        )
        for result in results
    ]

    # Highest final score first
    reranked.sort(
        key=lambda item: item["final_score"],
        reverse=True
    )

    # Reassign ranking after sorting
    for rank, result in enumerate(
        reranked,
        start=1
    ):

        result["rank"] = rank

    return reranked