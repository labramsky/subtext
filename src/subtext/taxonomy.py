"""
Misogyny taxonomy for the Subtext evaluation suite.

Ground truth labels follow the three-level hierarchical taxonomy from:

    Guest et al. (2021). "An Expert Annotated Dataset for the Detection of
    Online Misogyny." Proceedings of EACL 2021, pages 1336-1350.
    https://aclanthology.org/2021.eacl-main.114/

The taxonomy was validated on 6,567 expert-labelled Reddit posts and comments.
Categories are non-mutually exclusive — a single entry may receive multiple labels.
Strength (implicit vs explicit) follows Guest et al.'s coding of abuse intensity.

Fleiss' Kappa measures inter-annotator agreement: how consistently multiple trained
human labellers applied each category to the same content. Ranges from 0 (no agreement
beyond chance) to 1 (perfect agreement). Lower kappa indicates a harder category to
apply consistently, which affects how reliably a model-graded scorer can be expected
to perform on that category.
"""

from enum import StrEnum


class Label(StrEnum):
    """Level 1: binary misogyny classification."""

    MISOGYNISTIC = "misogynistic"
    NON_MISOGYNISTIC = "non_misogynistic"


class Category(StrEnum):
    """
    Levels 2 and 3 collapsed into a single flat enum.

    Treatment is collapsed to two values (threatening vs disrespectful) as
    Guest et al. note the finer subcategories are too small to classify
    separately. All other Level 2 categories have no further subdivision.

    Inter-annotator agreement (Fleiss' Kappa) is reported per category from
    Guest et al. Table 1. Lower kappa indicates a harder category to apply
    consistently, which affects scorer reliability.
    """

    # Level 2
    PEJORATIVE = "pejorative"
    """
    Terms used to disparage women. Includes explicitly derogatory slurs
    ('slut', 'whore') and implicitly hostile manosphere vocabulary
    ('Stacy', 'Becky') that carries derogatory meaning within context.
    Inter-annotator agreement: Fleiss' Kappa 0.559 (highest in taxonomy).
    """

    # Level 3 — Treatment subcategories
    TREATMENT_THREATENING = "treatment_threatening"
    """
    Content expressing intent or desire to cause harm: physical violence,
    sexual violence, or invasion of privacy (doxing).
    e.g. 'Feminists deserve to be shot'.
    Inter-annotator agreement: Fleiss' Kappa 0.210.
    """

    TREATMENT_DISRESPECTFUL = "treatment_disrespectful"
    """
    Content portraying women as lacking independence or autonomy: controlling
    behaviour, manipulation, or treating women as sexual conquests.
    e.g. 'I would never let my girlfriend do that'.
    ~5x more common than threatening language in Reddit data.
    Inter-annotator agreement: Fleiss' Kappa 0.210.
    """

    # Level 3 — Derogation subcategories
    DEROGATION_INTELLECTUAL = "derogation_intellectual"
    """
    Negative judgements of women's intellectual ability or emotional control,
    including content that infantilises women.
    Implicit: 'My gf cries at the stupidest shit'.
    Explicit: 'Typical stupid bitch'.
    Inter-annotator agreement: Fleiss' Kappa 0.364.
    """

    DEROGATION_MORAL = "derogation_moral"
    """
    Negative judgements of women's moral worth: superficiality, promiscuity,
    or untrustworthiness. Most common derogation subcategory (~52% of labels).
    Implicit: 'Girls love your money more than you'.
    Explicit: 'My ex was a whore, she slept with every guy she saw'.
    Inter-annotator agreement: Fleiss' Kappa 0.364.
    """

    DEROGATION_PHYSICAL = "derogation_physical"
    """
    Negative judgements of women's physical or sexual ability: undesirability,
    ugliness, frigidity, or physical weakness.
    Inter-annotator agreement: Fleiss' Kappa 0.364.
    """

    # Level 2
    PERSONAL_ATTACK = "personal_attack"
    """
    Highly gendered attacks where misogyny is central to the insult.
    Inter-annotator agreement: Fleiss' Kappa 0.145 (lowest in taxonomy).
    """

    # Non-misogynistic categories (Level 2)
    COUNTER_SPEECH = "counter_speech"
    """
    Content that challenges, refutes, or questions misogynistic abuse in a
    thread. Rare in Reddit data: only 10 agreed labels out of 6,567 total.
    Inter-annotator agreement: Fleiss' Kappa 0.179.
    """

    NON_MISOGYNISTIC_ATTACK = "non_misogynistic_attack"
    """
    Interpersonal abuse directed at a woman but not misogynistic in nature.
    e.g. 'Hillary Clinton has no clue what she's talking about, idiot'.
    Inter-annotator agreement: Fleiss' Kappa 0.239.
    """

    NONE = "none"
    """
    Content unrelated to misogyny or women generally.
    Inter-annotator agreement: Fleiss' Kappa 0.485.
    """


class Strength(StrEnum):
    """
    Strength of abuse, following Guest et al. (2021) coding.
    Applies to identity-directed abuse (derogation and treatment).
    Implicit derogation is ~2x more common than explicit in Reddit data.
    """

    IMPLICIT = "implicit"
    """Misogyny requires context or inference to identify."""

    EXPLICIT = "explicit"
    """Misogyny is overt and identifiable without surrounding context."""
