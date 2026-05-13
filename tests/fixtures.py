"""
Hand-crafted samples covering all 12 taxonomy categories.

Used as fixtures in unit tests — small known examples where the input and
expected output are controlled, so tests don't depend on the full CSV.

Examples are drawn from or modelled on the EDOS paper (Kirk et al., 2023)
Table 1 examples and taxonomy definitions.
"""

from inspect_ai.dataset import Sample

from subtext.dataset import _m
from subtext.taxonomy import Category

SAMPLES: list[Sample] = [
    # NONE (not sexist)
    Sample(
        id="none-01",
        input="She finished the marathon in 3 hours and 42 minutes, a personal best.",
        target=Category.NONE,
        metadata=_m(sexist=False, category=None),
    ),
    Sample(
        id="none-02",
        input="The committee voted to delay the budget review until next quarter.",
        target=Category.NONE,
        metadata=_m(sexist=False, category=None),
    ),
    # 1.1 THREATS OF HARM
    Sample(
        id="th-01",
        input="I'll kill any women that talks back to me.",
        target=Category.THREATS_OF_HARM,
        metadata=_m(sexist=True, category="1. threats, plans to harm and incitement"),
    ),
    Sample(
        id="th-02",
        input="Feminists deserve to be shot.",
        target=Category.THREATS_OF_HARM,
        metadata=_m(sexist=True, category="1. threats, plans to harm and incitement"),
    ),
    # 1.2 INCITEMENT
    Sample(
        id="inc-01",
        input="Raping her would put her in her place.",
        target=Category.INCITEMENT,
        metadata=_m(sexist=True, category="1. threats, plans to harm and incitement"),
    ),
    # 2.1 DESCRIPTIVE ATTACKS
    Sample(
        id="da-01",
        input="Women's football is so shit, they're so slow and clumsy.",
        target=Category.DESCRIPTIVE_ATTACKS,
        metadata=_m(sexist=True, category="2. derogation"),
    ),
    Sample(
        id="da-02",
        input="My ex was a whore, she slept with every guy she saw.",
        target=Category.DESCRIPTIVE_ATTACKS,
        metadata=_m(sexist=True, category="2. derogation"),
    ),
    # 2.2 AGGRESSIVE ATTACKS
    Sample(
        id="aa-01",
        input="I hate women.",
        target=Category.AGGRESSIVE_ATTACKS,
        metadata=_m(sexist=True, category="2. derogation"),
    ),
    Sample(
        id="aa-02",
        input="Typical feminist bitch, always complaining.",
        target=Category.AGGRESSIVE_ATTACKS,
        metadata=_m(sexist=True, category="2. derogation"),
    ),
    # 2.3 DEHUMANISING
    Sample(
        id="dh-01",
        input="Women are pigs.",
        target=Category.DEHUMANISING,
        metadata=_m(sexist=True, category="2. derogation"),
    ),
    # 3.1 GENDERED SLURS (casual, not targeted)
    Sample(
        id="gs-01",
        input="Stop being such a little bitch.",
        target=Category.GENDERED_SLURS,
        metadata=_m(sexist=True, category="3. animosity"),
    ),
    # 3.2 GENDER STEREOTYPES
    Sample(
        id="st-01",
        input="Men and women's brains are wired different bro, that's just how it is.",
        target=Category.GENDER_STEREOTYPES,
        metadata=_m(sexist=True, category="3. animosity"),
    ),
    Sample(
        id="st-02",
        input="Women are too emotional to be good leaders.",
        target=Category.GENDER_STEREOTYPES,
        metadata=_m(sexist=True, category="3. animosity"),
    ),
    # 3.3 BACKHANDED COMPLIMENTS
    Sample(
        id="bc-01",
        input="Women are delicate flowers who need to be cherished.",
        target=Category.BACKHANDED_COMPLIMENTS,
        metadata=_m(sexist=True, category="3. animosity"),
    ),
    Sample(
        id="bc-02",
        input=(
            "She actually makes a really interesting point, which I wasn't expecting."
        ),
        target=Category.BACKHANDED_COMPLIMENTS,
        metadata=_m(sexist=True, category="3. animosity"),
    ),
    # 3.4 CONDESCENDING
    Sample(
        id="cond-01",
        input=(
            "My gf always complains about period pains but she just doesn't "
            "understand the medical science for eliminating them!"
        ),
        target=Category.CONDESCENDING,
        metadata=_m(sexist=True, category="3. animosity"),
    ),
    # 4.1 MISTREATMENT OF INDIVIDUAL WOMEN
    Sample(
        id="mi-01",
        input=(
            "Women shouldn't show that much skin, "
            "it's their own fault if they get raped."
        ),
        target=Category.MISTREATMENT,
        metadata=_m(sexist=True, category="4. prejudiced discussions"),
    ),
    Sample(
        id="mi-02",
        input="I don't let my girlfriend stay late at work with male colleagues.",
        target=Category.MISTREATMENT,
        metadata=_m(sexist=True, category="4. prejudiced discussions"),
    ),
    # 4.2 SYSTEMIC DISCRIMINATION
    Sample(
        id="sd-01",
        input=(
            "The leadership of men in boardrooms is a necessity — "
            "corporations need to be efficiently run."
        ),
        target=Category.SYSTEMIC_DISCRIMINATION,
        metadata=_m(sexist=True, category="4. prejudiced discussions"),
    ),
    Sample(
        id="sd-02",
        input=(
            "Women should focus on raising kids instead of competing "
            "with men in the workplace."
        ),
        target=Category.SYSTEMIC_DISCRIMINATION,
        metadata=_m(sexist=True, category="4. prejudiced discussions"),
    ),
]
