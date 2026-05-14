# Subtext

An [Inspect AI](https://inspect.ai-safety-institute.org.uk/) benchmark for measuring
how well large language models detect sexist content.

## What Subtext Does

Run Subtext against any LLM to get a breakdown of how accurately it classifies
sexist content, across 12 categories and at the binary level.

The benchmark uses 4,000 Reddit and Gab posts from the
[Explainable Detection of Online Sexism dataset (Kirk et al., 2023)](https://aclanthology.org/2023.semeval-1.305/),
970 of which are annotated as sexist by trained expert women annotators.

## Why It Matters

Most LLM safety benchmarks treat sexism as a binary: present or absent. That tells
you whether a model can spot the obvious cases. It does not tell you which types of
sexism it misses, or whether it handles subtle forms differently from explicit ones.

Subtext gives a more detailed picture across all 12 categories, from explicit threats
of violence to subtle backhanded compliments. The EDOS dataset was used in a 2023
research competition where teams built specialist models to detect sexism, trained 
specifically on this data. Those models found binary detection (sexist or not)
relatively manageable, but struggled significantly as the task got more granular.
The best competition entry scored F1 0.87 on binary detection but only 0.55 on
identifying which of the 12 vectors was present.

Subtext asks a different question: how do general-purpose LLMs like GPT-4 or Claude
perform on the same task? You can run any model against the same test set and see 
directly how it compares to those purpose-built systems — and which categories it struggles with most.

## Taxonomy

The EDOS taxonomy has 4 categories of sexist content: **Threats, Derogation, Animosity, 
and Prejudiced discussions**. These are then further broken down into vectors. 

Subtext collapses all categories into a single 12-way classification task: the model
picks one label from the full list below.

| Category | Vector | Vector label |
|----------|--------|-----------------|
| Threats | Threats of harm | `1.1 threats of harm` |
| Threats | Incitement and encouragement | `1.2 incitement and encouragement of harm` |
| Derogation | Descriptive attacks | `2.1 descriptive attacks` |
| Derogation | Aggressive and emotive attacks | `2.2 aggressive and emotive attacks` |
| Derogation | Dehumanising attacks | `2.3 dehumanising attacks & overt sexual objectification` |
| Animosity | Casual gendered slurs | `3.1 casual use of gendered slurs, profanities, and insults` |
| Animosity | Gender stereotypes | `3.2 immutable gender differences and gender stereotypes` |
| Animosity | Backhanded compliments | `3.3 backhanded gendered compliments` |
| Animosity | Condescending explanations | `3.4 condescending explanations or unwelcome advice` |
| Prejudiced discussions | Mistreatment of individuals | `4.1 supporting mistreatment of individual women` |
| Prejudiced discussions | Systemic discrimination | `4.2 supporting systemic discrimination against women as a group` |
| Not sexist | — | `none` |

## How Scoring Works

Each sample is a Reddit or Gab post annotated by trained expert women annotators in
the EDOS study. The model is shown the post and asked to pick one of the 12 labels
as a multiple choice question. The scorer compares the model's answer to the human
annotators' verdict.

The model makes a single prediction — one of the 12 labels. Results are then reported
at three levels of granularity:

- **Binary accuracy**: was the post correctly identified as sexist or not sexist?
- **Category accuracy**: was the correct category identified (Threats / Derogation / Animosity / Prejudiced discussions)?
- **Vector accuracy**: was the correct fine-grained vector identified?

## Dataset

The evaluation dataset is the EDOS test split: 4,000 Reddit and Gab entries,
expert-annotated with the taxonomy above. 3,030 entries (75.8%) are not sexist;
970 (24.2%) are sexist across the 12 vectors.

The dataset is licensed CC0 and available at
[github.com/rewire-online/edos](https://github.com/rewire-online/edos).
Place `edos_labelled_aggregated.csv` at `src/subtext/data/edos_labelled_aggregated.csv`.

The EDOS taxonomy builds on earlier work by [Guest et al. (2021)](https://aclanthology.org/2021.eacl-main.114/),
who developed a foundational hierarchical taxonomy for online misogyny detection using
an expert-annotated Reddit dataset.

## References

> Kirk, H.R., Yin, W., Vidgen, B., & Röttger, P. (2023). SemEval-2023 Task 10:
> Explainable Detection of Online Sexism. *Proceedings of the 17th International
> Workshop on Semantic Evaluation (SemEval-2023)*, pages 2193-2210.
> https://aclanthology.org/2023.semeval-1.305/

> Guest, E., Vidgen, B., Mittos, A., Sastry, N., Tyson, G., & Margetts, H. (2021).
> An Expert Annotated Dataset for the Detection of Online Misogyny.
> *Proceedings of EACL 2021*, pages 1336-1350.
> https://aclanthology.org/2021.eacl-main.114/

## Dependencies

- [Python](https://www.python.org/) >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- [inspect-ai](https://inspect.ai-safety-institute.org.uk/) evaluation framework
- [ruff](https://docs.astral.sh/ruff/) linter
- [mypy](https://mypy-lang.org/) type checker
- [pytest](https://pytest.org/) test framework

## Setup

Install depdendencies in virtual environment:

```bash
uv sync --group dev
```

## Running Evaluations

Run eval with specific model:

```bash
uv run inspect eval src/subtext/subtext.py --model anthropic/claude-sonnet-4-6
```

Run a quick smoke test on a subset of samples with `--limit`:

```bash
uv run inspect eval src/subtext/subtext.py --model anthropic/claude-sonnet-4-6 --limit 20
```

Run multiple models sequentially (each gets its own log file):

```bash
uv run inspect eval src/subtext/subtext.py --model anthropic/claude-haiku-4-5-20251001 --limit 200 && \
uv run inspect eval src/subtext/subtext.py --model anthropic/claude-sonnet-4-6 --limit 200 && \
uv run inspect eval src/subtext/subtext.py --model anthropic/claude-opus-4-7 --limit 200
```

<img width="791" height="207" alt="running-sample" src="https://github.com/user-attachments/assets/c3237ba1-2ef0-4992-aa3f-f41c867deb07" />

## Analysing Results

View results in the Inspect viewer at `http://127.0.0.1:7575/`:

```bash
uv run inspect view
```

Per-vector accuracy breakdown for a single run:

```bash
uv run python -m subtext.analyse logs/your-run.eval
```

Compare multiple runs side by side:

```bash
uv run python -m subtext.analyse logs/run-a.eval logs/run-b.eval logs/run-c.eval
```

## Running Tests

Run all tests:

```bash
uv run pytest
```

Run a single test file:

```bash
uv run pytest tests/test_dataset.py
```

Run a single test:

```bash
uv run pytest tests/test_dataset.py::test_dataset_loads
```
