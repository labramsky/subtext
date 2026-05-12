# Subtext

An [Inspect AI](https://inspect.ai-safety-institute.org.uk/) benchmark for measuring
how well large language models detect implicit misogynistic content.

## What Subtext Does

Subtext tests any LLM's ability to classify text against the Guest et al. (2021)
misogyny taxonomy — a three-level hierarchy built from 6,567 expert-annotated Reddit
posts. Run it against a model to get a breakdown of classification accuracy by category
and by implicit vs explicit strength.

The benchmark runs against the Guest et al. held-out test split (1,303 of those 6,567
entries), keeping results directly comparable to prior work.

## Why Implicit Misogyny

Current LLM safety benchmarks mostly test for explicit harm — slurs, threats, overt
hostility. A model can pass those benchmarks and still fail systematically on subtle,
context-dependent misogyny.

Guest et al. (2021) found that automated classifiers have the highest misclassification
rates on **implicit derogation** — content where the misogyny requires context or
inference to identify. Morbidoni & Sarra (2023) showed GPT-3.5 outperforms BERT
classifiers overall, but did not measure the implicit/explicit gap at the category level.

Subtext fills that gap: it reports accuracy broken down by category and by
implicit vs explicit strength, using the same taxonomy and dataset as prior work so
results are directly comparable.

## Taxonomy

Categories follow Guest et al. (2021). Subcategories are collapsed into a single flat
classification task:

**Misogynistic:**
- `Misogynistic_pejorative` — slurs and manosphere vocabulary ('Stacy', 'Becky')
- `Treatment_threatening` — language expressing intent to cause harm
- `Treatment_disrespectful` — controlling, manipulative, or conquering treatment
- `Derogation_intellectual_inferiority` — demeaning women's intellect or emotional control
- `Derogation_moral_inferiority` — demeaning women's moral worth or trustworthiness
- `Derogation_sexual_or_physical_limitations` — demeaning women's physical or sexual worth
- `Derogation_other` — behaviour-based derogation (careers, finances, traditional roles)
- `Misogynistic_personal_attack` — gendered attacks where misogyny is central

**Non-misogynistic:**
- `Counter_speech` — content that challenges or refutes misogynistic abuse
- `Nonmisogynistic_personal_attack` — abuse directed at a woman but not misogynistic
- `None_of_the_categories` — content unrelated to misogyny

Each sample carries an implicit/explicit strength flag where coded. Strength is only
annotated for Treatment and Derogation categories in the source data.

## Dataset

The evaluation dataset is the Guest et al. (2021) test split: 1,303 Reddit posts and
comments, expert-annotated with the taxonomy above.

The dataset is not distributed with this repository. You can obtain `final_labels.csv` from the [EACL 2021 paper page](https://aclanthology.org/2021.eacl-main.114/) and place it at `src/subtext/data/final_labels.csv`.

## References

> Guest, E., Vidgen, B., Mittos, A., Sastry, N., Tyson, G., & Margetts, H. (2021).
> An Expert Annotated Dataset for the Detection of Online Misogyny.
> *Proceedings of EACL 2021*, pages 1336–1350.
> https://aclanthology.org/2021.eacl-main.114/

> Morbidoni, C., & Sarra, A. (2023). Can LLMs assist humans in assessing online
> misogyny? Experiments with GPT-3.5. *CEUR Workshop Proceedings*, Vol. 3571.
> https://ceur-ws.org/Vol-3571/regular1.pdf


## Dependencies

- [Python](https://www.python.org/) >= 3.12
- [uv](https://docs.astral.sh/uv/) — package manager
- [inspect-ai](https://inspect.ai-safety-institute.org.uk/) — evaluation framework
- [ruff](https://docs.astral.sh/ruff/) — linter
- [mypy](https://mypy-lang.org/) — type checker
- [pytest](https://pytest.org/) — test framework

## Setup

```bash
uv sync --group dev
```

## Running Evaluations

```bash
uv run inspect eval src/subtext/task.py --model openai/gpt-4o
```

## Running Tests

```bash
uv run pytest
```
