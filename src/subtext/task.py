"""
Inspect AI task for the Subtext evaluation.
"""

from string import ascii_uppercase

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice, system_message

from subtext.dataset import dataset as _load_dataset
from subtext.taxonomy import Category

CHOICES: list[str] = [c.value for c in Category]

_SYSTEM_PROMPT = (
    "You will be given a social media post. "
    "Select the label that best describes it."
)


def _task_dataset() -> MemoryDataset:
    samples = []
    for s in _load_dataset().samples:
        letter = ascii_uppercase[CHOICES.index(s.target)]
        samples.append(Sample(
            id=s.id,
            input=s.input,
            target=letter,
            choices=CHOICES,
            metadata=s.metadata,
        ))
    return MemoryDataset(samples, name="edos_2023")


@task
def subtext() -> Task:
    return Task(
        dataset=_task_dataset(),
        solver=[
            system_message(_SYSTEM_PROMPT),
            multiple_choice(),
        ],
        scorer=choice(),
    )
