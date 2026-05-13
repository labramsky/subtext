"""
Inspect AI dataset for the Subtext evaluation suite.

Each sample is a Reddit or Gab post from the EDOS test split, paired with the
human annotators' fine-grained sexism vector label and top-level category.

CSV -> Sample field mapping (edos_labelled_aggregated.csv)
----------------------------------------------------------
    CSV column        Sample field            Notes
    ──────────────────────────────────────────────────────────────
    rewire_id      ->  id                      stable identifier per entry
    text           ->  input                   the text the model classifies
    label_vector   ->  target                  one of 12 Category values;
                                               "none" for non-sexist entries,
                                               one of 11 vectors for sexist ones
    label_sexist   ->  metadata["sexist"]      "sexist" → True
                                               "not sexist" → False
    label_category ->  metadata["category"]    category string for sexist entries
                                               None for non-sexist entries
    split          ->  (filter only)           retain rows where split == "test"
"""

import csv
from pathlib import Path
from typing import Any

from inspect_ai.dataset import Dataset, MemoryDataset, Sample
from pydantic import BaseModel

from subtext.taxonomy import Category


class SampleMetadata(BaseModel, frozen=True):
    """
    Typed metadata schema for Subtext samples.

    Stored as a plain dict inside ``Sample.metadata`` (via ``.model_dump()``).
    Reconstruct the typed object inside a solver or scorer with::

        meta = state.metadata_as(SampleMetadata)
        if meta.sexist:
            ...

    Binary (sexist / not sexist) and category-level classification are both
    available as metadata, derived from the EDOS human annotations.
    """

    sexist: bool
    """Whether the entry is sexist. Derived from ``label_sexist`` in the CSV."""

    category: str | None
    """
    Task B category label for sexist entries. None for non-sexist entries.
    One of:
        "1. threats, plans to harm and incitement"
        "2. derogation"
        "3. animosity"
        "4. prejudiced discussions"
        None  (entry is not sexist)
    """


def _m(sexist: bool, category: str | None) -> dict[str, Any]:
    return SampleMetadata(sexist=sexist, category=category).model_dump(mode="json")


_CSV_PATH = Path(__file__).parent / "data" / "edos_labelled_aggregated.csv"


def _load_csv() -> list[Sample]:
    samples: list[Sample] = []
    with open(_CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["split"] != "test":
                continue
            sexist = row["label_sexist"] == "sexist"
            category = row["label_category"] if sexist else None
            samples.append(Sample(
                id=row["rewire_id"],
                input=row["text"],
                target=Category(row["label_vector"]),
                metadata=_m(sexist=sexist, category=category),
            ))
    return samples


def dataset() -> Dataset:
    """
    Return the Subtext evaluation dataset as an Inspect ``MemoryDataset``.

    Loads the EDOS test split from ``edos_labelled_aggregated.csv`` (4,000
    entries: 3,030 not sexist, 970 sexist across 11 fine-grained vectors).

    Basic usage in an Inspect task::

        from subtext.dataset import dataset

        @task
        def subtext() -> Task:
            return Task(dataset=dataset(), solver=[...], scorer=...)

    Filtering by metadata::

        from subtext.dataset import dataset
        from subtext.taxonomy import SEXIST_VECTORS

        d = dataset()
        sexist_only = d.filter(lambda s: s.metadata["sexist"])
        category_2  = d.filter(lambda s: s.metadata["category"] == "2. derogation")
    """
    return MemoryDataset(_load_csv(), name="edos_2023")
