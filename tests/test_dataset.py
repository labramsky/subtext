from subtext.dataset import dataset
from subtext.taxonomy import CATEGORY_LABELS, SEXIST_VECTORS, Category

VALID_CATEGORIES = {
    "1. threats, plans to harm and incitement",
    "2. derogation",
    "3. animosity",
    "4. prejudiced discussions",
}


def test_dataset_loads():
    d = dataset()
    print('d.samples', d.samples[0])
    assert len(d.samples) == 4000


def test_all_targets_are_valid_categories():
    d = dataset()
    valid = {c.value for c in Category}
    for sample in d.samples:
        assert sample.target in valid, f"unexpected target: {sample.target}"


def test_sexist_metadata_is_bool():
    d = dataset()
    for sample in d.samples:
        assert isinstance(sample.metadata["sexist"], bool)


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


def test_target_and_sexist_agree():
    d = dataset()
    for sample in d.samples:
        if sample.metadata["sexist"]:
            assert sample.target in SEXIST_VECTORS
        else:
            assert sample.target == Category.NONE


def test_sexist_vectors_are_subset_of_all_categories():
    assert SEXIST_VECTORS.issubset({c.value for c in Category})


def test_category_labels_covers_all_vectors():
    for cat in Category:
        assert cat in CATEGORY_LABELS


def test_no_missing_inputs():
    d = dataset()
    for sample in d.samples:
        assert sample.input and sample.input.strip()
