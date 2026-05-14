"""
Scorer and metrics for the Subtext evaluation.

A single scorer produces three accuracy metrics at different levels of granularity:

  binary   — was the post correctly identified as sexist or not?
  category — was the correct top-level category identified?
  vector   — was the correct fine-grained vector identified?

All three are derived from the same letter prediction and returned as a
dict-valued Score, with accuracy() and stderr() applied to each key.
"""

from inspect_ai.scorer import (
    Score,
    Scorer,
    Target,
    accuracy,
    answer,
    scorer,
    stderr,
)
from inspect_ai.solver import TaskState

from subtext.dataset import LETTER_TO_VECTOR
from subtext.taxonomy import SEXIST_VECTORS, VECTOR_CATEGORY


@scorer(metrics={
    "binary":   [accuracy(), stderr()],
    "category": [accuracy(), stderr()],
    "vector":   [accuracy(), stderr()],
})
def subtext_scorer() -> Scorer:
    # Use the built-in answer() scorer to extract the letter from "ANSWER: $LETTER"
    answer_scorer = answer("letter")

    async def score(state: TaskState, target: Target) -> Score:
        extracted = await answer_scorer(state, target)
        
        # Unscored if formatting failures 
        if not extracted.answer:
            return Score.unscored(answer="", explanation="no answer found")

        answer_char = extracted.answer.upper()

        # Incorrect if the model hallucinated a letter outside the valid range (A–L)
        if answer_char not in LETTER_TO_VECTOR:
            return Score(
                value={"binary": 0.0, "category": 0.0, "vector": 0.0},
                answer=answer_char,
                explanation=f"invalid letter: {answer_char}",
            )

        answer_vector = LETTER_TO_VECTOR[answer_char]
        target_vector = LETTER_TO_VECTOR[target.text]

        is_binary_correct = (answer_vector in SEXIST_VECTORS) == (
            target_vector in SEXIST_VECTORS
        )
        is_category_correct = (
            VECTOR_CATEGORY[answer_vector] == VECTOR_CATEGORY[target_vector]
        )
        is_vector_correct = answer_char == target.text

        return Score(
            value={
                "binary":   float(is_binary_correct),
                "category": float(is_category_correct),
                "vector":   float(is_vector_correct),
            },
            answer=answer_char,
            explanation=f"answer={answer_vector!r}, target={target_vector!r}",
        )

    return score
