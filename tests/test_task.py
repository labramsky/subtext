from string import ascii_uppercase

from inspect_ai import Task

from subtext.dataset import CHOICES
from subtext.task import subtext
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


def test_subtext_returns_task():
    assert isinstance(subtext(), Task)
