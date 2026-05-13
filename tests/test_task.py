from string import ascii_uppercase

from inspect_ai import Task
from inspect_ai.dataset import MemoryDataset

from subtext.task import CHOICES, _task_dataset, subtext
from subtext.taxonomy import Category


def test_choices_covers_all_categories():
    assert set(CHOICES) == {c.value for c in Category}


def test_choices_has_no_duplicates():
    assert len(CHOICES) == len(set(CHOICES))


def test_choices_length():
    assert len(CHOICES) == len(Category)


def test_each_category_maps_to_unique_letter():
    letters = [ascii_uppercase[CHOICES.index(c.value)] for c in Category]
    assert len(letters) == len(set(letters))


def test_task_dataset_returns_memory_dataset():
    assert isinstance(_task_dataset(), MemoryDataset)


def test_task_dataset_sample_count():
    assert len(_task_dataset().samples) == 4000


def test_task_dataset_targets_are_letters():
    valid = set(ascii_uppercase[: len(Category)])
    for sample in _task_dataset().samples:
        assert sample.target in valid


def test_task_dataset_all_samples_have_choices():
    for sample in _task_dataset().samples:
        assert sample.choices == CHOICES


def test_task_dataset_letter_roundtrips_to_vector():
    from subtext.dataset import dataset as _load_dataset

    source = {s.id: s for s in _load_dataset().samples}
    for sample in _task_dataset().samples:
        idx = ascii_uppercase.index(sample.target)
        assert CHOICES[idx] == source[sample.id].target


def test_task_dataset_preserves_id_and_input():
    from subtext.dataset import dataset as _load_dataset

    source = {s.id: s for s in _load_dataset().samples}
    for sample in _task_dataset().samples:
        assert sample.id in source
        assert sample.input == source[sample.id].input
        assert sample.metadata == source[sample.id].metadata


def test_subtext_returns_task():
    assert isinstance(subtext(), Task)
