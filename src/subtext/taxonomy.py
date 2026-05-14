"""
Sexism taxonomy for the Subtext evaluation suite.

Ground truth labels follow the three-level hierarchical taxonomy from:

    Kirk, H.R., Yin, W., Vidgen, B., & Röttger, P. (2023). SemEval-2023 Task 10:
    Explainable Detection of Online Sexism. Proceedings of SemEval-2023,
    pages 2193-2210. https://aclanthology.org/2023.semeval-1.305/

The full EDOS dataset covers ~20,000 social media entries (Reddit and Gab),
annotated by trained expert women annotators. The held-out test split
(4,000 entries) is used for evaluation. Labels are mutually exclusive at each level.

Taxonomy levels:
  Binary:     sexist vs. not sexist
  Categories: 4 categories of sexism
  Vectors:    12 vectors (11 sexist + "none" for not sexist)

This benchmark collapses to a 12-way classification. Binary and category results
are derived from the vector prediction.

Vector enum values match the ``label_vector`` field in the EDOS CSV exactly,
so ``Vector(row["label_vector"])`` works without a translation layer.
"""

from enum import StrEnum


class Vector(StrEnum):
    """
    12-way vector classification. Values match the ``label_vector`` field in
    the EDOS CSV exactly. Top-level category is encoded in the first character:
    "1." = threats, "2." = derogation, "3." = animosity, "4." = prejudiced.
    """

    # Not sexist
    NONE = "none"
    """Content that is not sexist."""

    # 1. Threats
    THREATS_OF_HARM = "1.1 threats of harm"
    """
    Expressing intent, willingness or desire to harm an individual woman or
    group of women (physical, sexual, emotional, or privacy-based harm).
    e.g. "I'll kill any women that talks back to me".
    """

    INCITEMENT = "1.2 incitement and encouragement of harm"
    """
    Inciting or encouraging an individual or audience to harm women.
    Includes rationalising or justifying such harm to others.
    e.g. "Raping her would put her in her place".
    """

    # 2. Derogation
    DESCRIPTIVE_ATTACKS = "2.1 descriptive attacks"
    """
    Characterising or describing women in a derogatory manner: negative
    generalisations about women's abilities, appearance, sexual behaviour,
    intellect, character, or morals.
    e.g. "Women's football is so shit, they're so slow and clumsy".
    """

    AGGRESSIVE_ATTACKS = "2.2 aggressive and emotive attacks"
    """
    Expressing strong negative sentiment against women — disgust, hatred,
    baseless accusations, or the use of gendered slurs or profanities.
    e.g. "I hate women".
    """

    DEHUMANISING = "2.3 dehumanising attacks & overt sexual objectification"
    """
    Derogating women by comparing them to non-human entities (vermin, disease,
    refuse), or overtly reducing them to sexual objects.
    e.g. "Women are pigs".
    """

    # 3. Animosity
    GENDERED_SLURS = "3.1 casual use of gendered slurs, profanities, and insults"
    """
    Using gendered slurs or profanities casually, not to intentionally attack
    women. Only terms that traditionally describe women are in scope.
    e.g. "Stop being such a little bitch".
    """

    GENDER_STEREOTYPES = "3.2 immutable gender differences and gender stereotypes"
    """
    Asserting immutable or essential differences between men and women.
    Includes sexist jokes framed as factual claims.
    e.g. "Men and women's brains are wired different bro, that's just how it is".
    """

    BACKHANDED_COMPLIMENTS = "3.3 backhanded gendered compliments"
    """
    Ostensibly complimenting women while actually belittling or implying their
    inferiority (e.g. reducing women to their attractiveness or framing them as
    innately weak or helpless).
    e.g. "Women are delicate flowers who need to be cherished".
    """

    CONDESCENDING = "3.4 condescending explanations or unwelcome advice"
    """
    Offering unsolicited or patronising advice to women on topics they know
    more about (mansplaining).
    e.g. "My gf always complains about period pains but she just doesn't
    understand the medical science for eliminating them!".
    """

    # 4. Prejudiced Discussions
    MISTREATMENT = "4.1 supporting mistreatment of individual women"
    """
    Expressing support for mistreatment of women as individuals — denying,
    understating, or justifying such mistreatment.
    e.g. "Women shouldn't show that much skin, it's their own fault if they get raped".
    """

    SYSTEMIC_DISCRIMINATION = (
        "4.2 supporting systemic discrimination against women as a group"
    )
    """
    Expressing support for systemic discrimination of women — denying,
    understating, or justifying such discrimination.
    e.g. "The leadership of men in boardrooms is a necessity — corporations
    need to be efficiently run".
    """


SEXIST_VECTORS: frozenset[str] = frozenset({
    Vector.THREATS_OF_HARM,
    Vector.INCITEMENT,
    Vector.DESCRIPTIVE_ATTACKS,
    Vector.AGGRESSIVE_ATTACKS,
    Vector.DEHUMANISING,
    Vector.GENDERED_SLURS,
    Vector.GENDER_STEREOTYPES,
    Vector.BACKHANDED_COMPLIMENTS,
    Vector.CONDESCENDING,
    Vector.MISTREATMENT,
    Vector.SYSTEMIC_DISCRIMINATION,
})
"""All sexist Vector values (excludes NONE)."""


VECTOR_CATEGORY: dict[str, str] = {
    Vector.THREATS_OF_HARM: "1. threats, plans to harm and incitement",
    Vector.INCITEMENT: "1. threats, plans to harm and incitement",
    Vector.DESCRIPTIVE_ATTACKS: "2. derogation",
    Vector.AGGRESSIVE_ATTACKS: "2. derogation",
    Vector.DEHUMANISING: "2. derogation",
    Vector.GENDERED_SLURS: "3. animosity",
    Vector.GENDER_STEREOTYPES: "3. animosity",
    Vector.BACKHANDED_COMPLIMENTS: "3. animosity",
    Vector.CONDESCENDING: "3. animosity",
    Vector.MISTREATMENT: "4. prejudiced discussions",
    Vector.SYSTEMIC_DISCRIMINATION: "4. prejudiced discussions",
    Vector.NONE: "none",
}
"""Maps each vector value to its category label string."""
