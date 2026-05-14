"""
Tests for subtext_scorer.

Letter-to-category mapping (from CHOICES order):
  A = none
  B = 1.1 threats of harm
  D = 2.1 descriptive attacks      (derogation)
  E = 2.2 aggressive and emotive attacks  (derogation)
  H = 3.2 gender stereotypes       (animosity)
"""

import math

import pytest
from inspect_ai.model import ModelName, ModelOutput
from inspect_ai.model._chat_message import ChatMessageUser
from inspect_ai.scorer import Target
from inspect_ai.solver import TaskState

from subtext.scorer import subtext_scorer


def make_state(completion: str) -> TaskState:
    return TaskState(
        model=ModelName("mockllm/model"),
        sample_id=0,
        epoch=0,
        input="test post",
        messages=[ChatMessageUser(content="test post")],
        output=ModelOutput.from_content(model="mockllm/model", content=completion),
    )


@pytest.mark.anyio
async def test_exact_match():
    score = await subtext_scorer()(make_state("ANSWER: D"), Target("D"))
    assert score.value == {"binary": 1.0, "category": 1.0, "vector": 1.0}


@pytest.mark.anyio
async def test_same_category_wrong_vector():
    # D=2.1 descriptive attacks, E=2.2 aggressive attacks — both derogation, both sexist
    score = await subtext_scorer()(make_state("ANSWER: E"), Target("D"))
    assert score.value == {"binary": 1.0, "category": 1.0, "vector": 0.0}


@pytest.mark.anyio
async def test_wrong_category_but_correct_binary():
    # D = 2.1 derogation, H = 3.2 animosity — both sexist, different category
    score = await subtext_scorer()(make_state("ANSWER: H"), Target("D"))
    assert score.value == {"binary": 1.0, "category": 0.0, "vector": 0.0}


@pytest.mark.anyio
async def test_wrong_binary():
    # A = none, B = threats — sexist vs not sexist
    score = await subtext_scorer()(make_state("ANSWER: B"), Target("A"))
    assert score.value == {"binary": 0.0, "category": 0.0, "vector": 0.0}


@pytest.mark.anyio
async def test_no_answer_is_unscored():
    score = await subtext_scorer()(make_state("I don't know"), Target("D"))
    assert math.isnan(score.as_float())


@pytest.mark.anyio
async def test_invalid_letter_is_incorrect():
    score = await subtext_scorer()(make_state("ANSWER: Z"), Target("D"))
    assert score.value == {"binary": 0.0, "category": 0.0, "vector": 0.0}


@pytest.mark.anyio
async def test_lowercase_answer_accepted():
    score = await subtext_scorer()(make_state("ANSWER: d"), Target("D"))
    assert score.value == {"binary": 1.0, "category": 1.0, "vector": 1.0}
