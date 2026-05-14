from string import ascii_uppercase

from subtext.dataset import VECTORS, dataset
from subtext.taxonomy import SEXIST_VECTORS, VECTOR_CATEGORY, Category

VALID_CATEGORIES = {VECTOR_CATEGORY[v] for v in SEXIST_VECTORS}

def test_dataset_loads():
    d = dataset()
    assert len(d.samples) == 4000


def test_target_and_sexist_agree():
    d = dataset()
    for sample in d.samples:
        vector = VECTORS[ascii_uppercase.index(sample.target)]
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
