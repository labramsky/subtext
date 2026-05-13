"""
Inspect AI task for the Subtext evaluation.
"""

from inspect_ai import Task, task
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice, system_message

from subtext.dataset import CHOICES as CHOICES  # re-export
from subtext.dataset import dataset

_SYSTEM_PROMPT = (
    "You will be given a social media post. "
    "Select the label that best describes it."
)


@task
def subtext() -> Task:
    return Task(
        dataset=dataset(),
        solver=[
            system_message(_SYSTEM_PROMPT),
            multiple_choice(),
        ],
        scorer=choice(),
    )
