import re

from app.schemas.query import QueryIntent


# =========================================================
# PRODUCT KEYWORDS
# =========================================================

PRODUCT_KEYWORDS = {

    "cement": [
        "cement",
        "portland cement",
        "opc",
        "ordinary portland cement",
        "portland slag cement",
        "psc",
        "portland pozzolana cement",
        "pozzolana cement",
        "ppc",
    ],

    "aggregate": [
        "aggregate",
        "coarse aggregate",
        "fine aggregate",
        "concrete aggregate",
    ],

    "steel": [
        "steel",
        "steel bar",
        "steel bars",
        "reinforcement steel",
        "reinforcement bar",
        "reinforcement bars",
        "rebar",
    ],

    "concrete": [
        "concrete",
        "reinforced concrete",
        "plain concrete",
        "plain and reinforced concrete",
    ],

    "brick": [
        "brick",
        "bricks",
        "brickwork",
    ],

    "medical_textile": [
        "medical textile",
        "medical textiles",
        "coverall",
        "protective coverall",
    ],
}


# =========================================================
# CEMENT TYPES
# =========================================================

CEMENT_TYPES = {

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
        "pozzolana cement",
        "ppc",
    ],
}


# =========================================================
# APPLICATION PATTERNS
# =========================================================

APPLICATION_PATTERNS = {

    "plain and reinforced concrete": [
        "plain and reinforced concrete",
        "plain and reinforced cement concrete",
    ],

    "reinforced concrete": [
        "reinforced concrete",
        "reinforced cement concrete",
        "rcc",
    ],

    "plain concrete": [
        "plain concrete",
    ],

    "structural concrete": [
        "structural concrete",
        "structural work",
        "structural construction",
    ],

    "building construction": [
        "building construction",
        "building work",
        "construction",
    ],

    "concrete construction": [
        "concrete construction",
    ],
}


# =========================================================
# STANDARD TYPE
# =========================================================

STANDARD_TYPE_PATTERNS = {

    "code_of_practice": [
        "code of practice",
        "design code",
        "design requirements",
        "design rules",
        "requirements for plain and reinforced concrete",
    ],

    "specification": [
        "product specification",
        "product requirements",
        "material specification",
        "cement specification",
    ],

    "test_method": [
        "test method",
        "method of test",
        "testing method",
        "testing",
    ],

    "guideline": [
        "guideline",
        "guidelines",
    ],
}

    


# =========================================================
# SPECIAL CONDITIONS
# =========================================================

SEISMIC_PATTERNS = [
    "seismic",
    "earthquake",
    "earthquake resistant",
    "earthquake-resistant",
    "ductile detailing",
    "ductile design",
    "seismic design",
]


FIRE_PATTERNS = [
    "fire resistance",
    "fire resistant",
    "fire-resistant",
    "fire safety",
    "fire protection",
]


ELECTRICAL_PATTERNS = [
    "electrical",
    "electronic",
    "electrical equipment",
    "electrical safety",
]


MEDICAL_PATTERNS = [
    "medical",
    "medical device",
    "medical textile",
    "healthcare",
    "hospital",
]


STRUCTURAL_PATTERNS = [
    "structural",
    "structural work",
    "structural construction",
    "load bearing",
    "load-bearing",
]


# =========================================================
# HELPER
# =========================================================

def contains_any(
    text: str,
    patterns: list[str]
) -> bool:

    return any(
        pattern in text
        for pattern in patterns
    )


# =========================================================
# GRADE EXTRACTION
# =========================================================

def extract_grade(
    text: str
):

    """
    Extract cement grade only when the number is explicitly
    associated with the word 'grade'.

    This prevents values such as:

        IS 269:2013

    from being incorrectly interpreted as grade 2013.
    """

    match = re.search(
        r"\b(33|43|53)\s*[-]?\s*grade\b",
        text
    )

    if match:
        return match.group(1)

    return None


# =========================================================
# APPLICATION EXTRACTION
# =========================================================

def extract_application(
    text: str
):

    matches = []

    for application, patterns in APPLICATION_PATTERNS.items():

        for pattern in patterns:

            if pattern in text:

                matches.append(
                    (
                        len(pattern),
                        application
                    )
                )

    if not matches:
        return None

    # Longest matching phrase wins.
    matches.sort(
        reverse=True
    )

    return matches[0][1]


# =========================================================
# STANDARD TYPE EXTRACTION
# =========================================================

def extract_standard_type(
    text: str
):

    for standard_type, patterns in STANDARD_TYPE_PATTERNS.items():

        if contains_any(
            text,
            patterns
        ):
            return standard_type

    return None


# =========================================================
# QUERY UNDERSTANDING
# =========================================================

def understand_query(
    query: str
) -> QueryIntent:

    text = query.lower().strip()

    intent = QueryIntent(
        raw_query=query
    )

    # -----------------------------------------------------
    # PRODUCT
    # -----------------------------------------------------

    for product, keywords in PRODUCT_KEYWORDS.items():

        if contains_any(
            text,
            keywords
        ):

            intent.product = product
            break

    # -----------------------------------------------------
    # CEMENT TYPE
    # -----------------------------------------------------

    for cement_type, keywords in CEMENT_TYPES.items():

        if contains_any(
            text,
            keywords
        ):

            intent.cement_type = cement_type
            break

    # -----------------------------------------------------
    # GRADE
    # -----------------------------------------------------

    intent.grade = extract_grade(text)

    # -----------------------------------------------------
    # APPLICATION
    # -----------------------------------------------------

    intent.application = extract_application(text)

    # -----------------------------------------------------
    # STRUCTURAL USE
    # -----------------------------------------------------

    if contains_any(
        text,
        STRUCTURAL_PATTERNS
    ):

        intent.structural_use = True

    # Reinforced concrete implies structural context
    # for this procurement-oriented prototype.
    if intent.application == "reinforced concrete":

        intent.structural_use = True

    # Plain + reinforced concrete is also structural
    # construction context.
    if (
        intent.application
        == "plain and reinforced concrete"
    ):

        intent.structural_use = True

    # -----------------------------------------------------
    # SEISMIC
    # -----------------------------------------------------

    if contains_any(
        text,
        SEISMIC_PATTERNS
    ):

        intent.seismic_requirement = True

    # -----------------------------------------------------
    # FIRE
    # -----------------------------------------------------

    if contains_any(
        text,
        FIRE_PATTERNS
    ):

        intent.fire_requirement = True

    # -----------------------------------------------------
    # ELECTRICAL
    # -----------------------------------------------------

    if contains_any(
        text,
        ELECTRICAL_PATTERNS
    ):

        intent.electrical_requirement = True

    # -----------------------------------------------------
    # MEDICAL
    # -----------------------------------------------------

    if contains_any(
        text,
        MEDICAL_PATTERNS
    ):

        intent.medical_requirement = True

    # -----------------------------------------------------
    # STANDARD TYPE
    # -----------------------------------------------------

    intent.standard_type = extract_standard_type(
        text
    )

    return intent


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    queries = [

        "ordinary Portland cement for building construction",

        "cement for reinforced concrete structural work",

        "53 grade Portland cement",

        "coarse aggregate for concrete",

        "requirements for plain and reinforced concrete",

        "seismic design of reinforced concrete structures",

    ]

    for query in queries:

        print("\n" + "=" * 70)

        print("QUERY:")
        print(query)

        print("\nINTENT:")

        intent = understand_query(query)

        print(
            intent.model_dump(
                exclude={
                    "raw_query"
                }
            )
        )