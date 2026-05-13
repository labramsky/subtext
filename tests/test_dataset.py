from string import ascii_uppercase

from subtext.dataset import CHOICES, dataset
from subtext.taxonomy import CATEGORY_LABELS, SEXIST_VECTORS, Category

VALID_CATEGORIES = {CATEGORY_LABELS[v] for v in SEXIST_VECTORS}

def test_dataset_loads():
    d = dataset()
    assert len(d.samples) == 4000


def test_target_and_sexist_agree():
    d = dataset()
    for sample in d.samples:
        vector = CHOICES[ascii_uppercase.index(sample.target)]
        if sample.metadata["sexist"]:
            assert vector in SEXIST_VECTORS
        else:
            assert vector == Category.NONE


def test_category_none_for_nonsexist():
    d = dataset()
    for sample in d.samples:
        if not sample.metadata["sexist"]:
            assert sample.metadata["category"] is None


def test_category_set_for_sexist():
    d = dataset()
    for sample in d.samples:
        if sample.metadata["sexist"]:
            assert sample.metadata["category"] in VALID_CATEGORIES


def test_no_missing_inputs():
    d = dataset()
    for sample in d.samples:
        assert sample.input and sample.input.strip()
