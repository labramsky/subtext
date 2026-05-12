"""
Misogyny taxonomy for the Subtext evaluation suite.

Ground truth labels follow the three-level hierarchical taxonomy from:

    Guest et al. (2021). "An Expert Annotated Dataset for the Detection of
    Online Misogyny." Proceedings of EACL 2021, pages 1336-1350.
    https://aclanthology.org/2021.eacl-main.114/

The taxonomy was developed and annotated across a corpus of 6,567 Reddit posts and
comments. The held-out test split (1,303 entries) is used for evaluation.
Categories are non-mutually exclusive — a single entry may receive multiple labels.

Enum values match the field values used in the Guest et al. CSV dataset exactly,
so that CSV rows can be mapped to taxonomy types without a translation layer.
For Treatment and Derogation subcategories (which are derived from two CSV columns,
level_2 and level_3), values follow the same naming convention as the CSV.
Use ``category_from_row()`` to resolve a CSV row to a Category.

Strength (implicit vs explicit) is only coded in the dataset for Derogation and
Treatment entries. Pejorative, Personal Attack, Counter Speech, and None carry no
strength annotation in the source data.

Fleiss' Kappa measures inter-annotator agreement: how consistently multiple trained
human labellers applied each category to the same content. Ranges from 0 (no agreement
beyond chance) to 1 (perfect agreement). Lower kappa indicates a harder category to
apply consistently, which affects how reliably a model-graded scorer can be expected
to perform on that category.
"""

from enum import StrEnum


class Category(StrEnum):
    """
    Levels 2 and 3 collapsed into a single flat enum.

    Treatment is collapsed to two values (threatening vs disrespectful) as
    Guest et al. note the finer subcategories are too small to classify
    separately. Derogation is split into four values following level_3.

    Values match the Guest et al. CSV dataset: level_2 field values where
    the category maps directly to a level_2 value; level_3-derived convention
    for Treatment and Derogation subcategories. Use ``category_from_row()``
    to map a CSV row to a Category.

    Inter-annotator agreement (Fleiss' Kappa) is reported per category from
    Guest et al. Table 1. Lower kappa indicates a harder category to apply
    consistently, which affects scorer reliability.
    """

    # Level 2 — direct CSV level_2 value
    PEJORATIVE = "Misogynistic_pejorative"
    """
    Terms used to disparage women. Includes explicitly derogatory slurs
    ('slut', 'whore') and implicitly hostile manosphere vocabulary
    ('Stacy', 'Becky') that carries derogatory meaning within context.
    Strength is not coded for this category in the Guest et al. dataset.
    Inter-annotator agreement: Fleiss' Kappa 0.559 (highest in taxonomy).
    """

    # Level 3 — Treatment subcategories (level_2 = "Treatment")
    TREATMENT_THREATENING = "Treatment_threatening"
    """
    Content expressing intent or desire to cause harm: physical violence,
    sexual violence, or invasion of privacy (doxing).
    CSV level_3 values: Threatening_Physical_violence, Threatening_Sexual_violence,
    Threatening_Privacy.
    e.g. 'Feminists deserve to be shot'.
    Inter-annotator agreement: Fleiss' Kappa 0.210.
    """

    TREATMENT_DISRESPECTFUL = "Treatment_disrespectful"
    """
    Content portraying women as lacking independence or autonomy: controlling
    behaviour, manipulation, or treating women as sexual conquests.
    CSV level_3 values: Disrespectful_actions_Seduction_and_conquest,
    Disrespectful_actions_Controlling, Disrespectful_actions_Manipulation,
    Disrespectful_actions_Other.
    e.g. 'I would never let my girlfriend do that'.
    ~5x more common than threatening language in Reddit data.
    Inter-annotator agreement: Fleiss' Kappa 0.210.
    """

    # Level 3 — Derogation subcategories (level_2 = "Derogation")
    DEROGATION_INTELLECTUAL = "Derogation_intellectual_inferiority"
    """
    Negative judgements of women's intellectual ability or emotional control,
    including content that infantilises women.
    CSV level_3 value: Intellectual_inferiority.
    Implicit: 'My gf cries at the stupidest shit'.
    Explicit: 'Typical stupid bitch'.
    Inter-annotator agreement: Fleiss' Kappa 0.364.
    """

    DEROGATION_MORAL = "Derogation_moral_inferiority"
    """
    Negative judgements of women's moral worth: superficiality, promiscuity,
    or untrustworthiness. Most common derogation subcategory (~52% of labels).
    CSV level_3 value: Moral_inferiority.
    Implicit: 'Girls love your money more than you'.
    Explicit: 'My ex was a whore, she slept with every guy she saw'.
    Inter-annotator agreement: Fleiss' Kappa 0.364.
    """

    DEROGATION_PHYSICAL = "Derogation_sexual_or_physical_limitations"
    """
    Negative judgements of women's physical or sexual ability: undesirability,
    ugliness, frigidity, or physical weakness.
    CSV level_3 value: Sexual_or_physical_limitations.
    Inter-annotator agreement: Fleiss' Kappa 0.364.
    """

    DEROGATION_OTHER = "Derogation_other"
    """
    Derogation based on women's behaviour rather than their inherent attributes.
    Covers three themes from the annotator codebook that were not given separate
    level_3 codes in the final dataset:
      - Financial ability: 'Women don't know how to negotiate salary'
      - Careers: demeaning women for feminine jobs or belittling them in male ones
      - Traditional gender roles: 'Women should get back in the kitchen'
    Also captures generic derogation that fits none of the above:
      - Implicit: 'I don't like women'
      - Explicit: 'All women should shut the fuck up'
    Represents 28% of derogation labels (79 of 285 entries). CSV level_3 value: Other.
    Inter-annotator agreement: Fleiss' Kappa 0.364 (shared with other derogation).
    """

    # Level 2 — direct CSV level_2 value
    PERSONAL_ATTACK = "Misogynistic_personal_attack"
    """
    Highly gendered attacks where misogyny is central to the insult.
    Strength is not coded for this category in the Guest et al. dataset.
    Inter-annotator agreement: Fleiss' Kappa 0.145 (lowest in taxonomy).
    """

    # Non-misogynistic categories (Level 2) — direct CSV level_2 values
    COUNTER_SPEECH = "Counter_speech"
    """
    Content that challenges, refutes, or questions misogynistic abuse in a
    thread. Rare in Reddit data: only 10 agreed labels out of 6,567 total.
    Inter-annotator agreement: Fleiss' Kappa 0.179.
    """

    NON_MISOGYNISTIC_ATTACK = "Nonmisogynistic_personal_attack"
    """
    Interpersonal abuse directed at a woman but not misogynistic in nature.
    e.g. 'Hillary Clinton has no clue what she's talking about, idiot'.
    Inter-annotator agreement: Fleiss' Kappa 0.239.
    """

    NONE = "None_of_the_categories"
    """
    Content unrelated to misogyny or women generally.
    Inter-annotator agreement: Fleiss' Kappa 0.485.
    """


MISOGYNISTIC_CATEGORIES: frozenset[str] = frozenset({
    Category.PEJORATIVE,
    Category.TREATMENT_THREATENING,
    Category.TREATMENT_DISRESPECTFUL,
    Category.DEROGATION_INTELLECTUAL,
    Category.DEROGATION_MORAL,
    Category.DEROGATION_PHYSICAL,
    Category.DEROGATION_OTHER,
    Category.PERSONAL_ATTACK,
})
"""
The set of Category values that constitute misogynistic content.
Derive binary classification from a sample's ``target`` field:

    is_misogynistic = sample.target in MISOGYNISTIC_CATEGORIES
"""


class Strength(StrEnum):
    """
    Strength of abuse, following Guest et al. (2021) coding.

    Only applies to Treatment and Derogation categories — Pejorative,
    Personal Attack, Counter Speech, and None carry no strength annotation
    in the source data.

    In the dataset: implicit derogation (182) is ~2x more common than
    explicit derogation (103). Implicit treatment (85) is ~5x more common
    than explicit treatment (18).
    """

    IMPLICIT = "implicit"
    """Misogyny requires context or inference to identify."""

    EXPLICIT = "explicit"
    """Misogyny is overt and identifiable without surrounding context."""


# ---------------------------------------------------------------------------
# CSV parsing helpers
#
# Maps raw Guest et al. CSV field values to taxonomy types.
# Used by the dataset loader; kept here so the mapping stays co-located
# with the taxonomy definitions it references.
# ---------------------------------------------------------------------------

_TREATMENT_FROM_LEVEL3: dict[str, Category] = {
    "Threatening_Physical_violence": Category.TREATMENT_THREATENING,
    "Threatening_Sexual_violence": Category.TREATMENT_THREATENING,
    "Threatening_Privacy": Category.TREATMENT_THREATENING,
    "Disrespectful_actions_Seduction_and_conquest": Category.TREATMENT_DISRESPECTFUL,
    "Disrespectful_actions_Controlling": Category.TREATMENT_DISRESPECTFUL,
    "Disrespectful_actions_Manipulation": Category.TREATMENT_DISRESPECTFUL,
    "Disrespectful_actions_Other": Category.TREATMENT_DISRESPECTFUL,
}

_DEROGATION_FROM_LEVEL3: dict[str, Category] = {
    "Intellectual_inferiority": Category.DEROGATION_INTELLECTUAL,
    "Moral_inferiority": Category.DEROGATION_MORAL,
    "Sexual_or_physical_limitations": Category.DEROGATION_PHYSICAL,
    "Other": Category.DEROGATION_OTHER,
}

STRENGTH_FROM_CSV: dict[str, Strength] = {
    "Nature of the abuse is Implicit": Strength.IMPLICIT,
    "Nature of the abuse is Explicit": Strength.EXPLICIT,
}
"""Maps raw CSV strength field values to ``Strength`` enum members."""


def category_from_row(level_2: str, level_3: str) -> Category:
    """
    Resolve a Guest et al. CSV row to a ``Category``.

    Treatment and Derogation require both level_2 and level_3 to determine
    the subcategory. All other categories map directly from level_2.

    Raises ``KeyError`` for unrecognised level_2/level_3 combinations.
    """
    if level_2 == "Treatment":
        return _TREATMENT_FROM_LEVEL3[level_3]
    if level_2 == "Derogation":
        return _DEROGATION_FROM_LEVEL3[level_3]
    return Category(level_2)
