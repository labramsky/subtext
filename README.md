# Subtext

An [Inspect AI](https://inspect.ai-safety-institute.org.uk/) evaluation suite for
measuring whether large language models produce implicit misogynistic content.

## What Subtext Evaluates

Subtext measures the tendency of LLMs to produce misogynistic content across a range
of prompt types. Scoring is grounded in the Guest et al. (2021) taxonomy
(see [Theoretical Basis](#theoretical-basis)):

- **Misogynistic pejoratives** — explicit slurs and implicit manosphere vocabulary
- **Misogynistic treatment** — threatening language and disrespectful portrayals of how women should be treated
- **Misogynistic derogation** — content demeaning women's intellect, morality, or physical worth
- **Gendered personal attacks** — highly gendered insults where misogyny is central

## Why It Matters

Current LLM safety evaluations mostly test for explicit harm — slurs, threats, overt
hostility. A model can pass those benchmarks and still systematically produce subtle,
context-dependent misogyny that real users encounter every day.

Subtext targets the gap. Its research question is whether models that pass standard
safety benchmarks still produce **implicit** abuse across the taxonomy categories —
implicit pejoratives, implicit controlling treatment, implicit moral derogation — content
that looks benign in isolation but is harmful in context. This is exactly the class of
content that Guest et al. (2021) found existing classifiers fail on, and that safety
training is least likely to address.

This matters for four reasons:

1. **Scale.** A model deployed to millions of users producing implicit misogyny in 1% of
   responses causes more aggregate harm than a rare explicit failure that gets caught
   and patched.
2. **Trust.** Implicit misogyny is harder for users to identify and push back on. A
   response that frames a woman as emotionally unstable without using a single slur
   feels more credible, not less.
3. **Accountability gap.** Safety teams can't improve what they can't measure. Subtext
   gives them a tool for a class of harm that currently has no rigorous benchmark.
4. **Model differentiation.** As models improve at avoiding explicit content, implicit
   abuse becomes the meaningful axis of comparison between them.

## Research Contribution

Subtext builds directly on two key failure modes Guest et al. identified in their own
work:

1. **Their classifier failed most on implicit derogation.** They built a detection tool;
   Subtext asks whether the models being deployed are producing exactly what that tool
   fails to catch.
2. **Their dataset was Reddit-specific.** They explicitly flag generalisability as a
   limitation. Subtext moves the question from "can we detect misogyny in Reddit posts"
   to "do LLMs produce it in response to prompts" — a different and more
   deployment-relevant context.

The value Subtext adds is closing the loop. Guest et al. gave us a validated taxonomy
and showed where automated detection breaks down. Subtext uses that taxonomy as ground
truth to evaluate whether models deployed at scale are producing the content that
detection systems miss — implicit, context-dependent misogyny across all four abuse
categories.

That makes it actionable in a way the original research was not. Guest et al. produced
a labelled dataset for training classifiers. Subtext produces a benchmark safety teams
can run against any model, track across versions, and use to demonstrate whether
fine-tuning is actually reducing subtle misogynistic outputs or just suppressing the
explicit content that was already easy to catch.

## Theoretical Basis

### Guest et al. (2021) — Misogyny Taxonomy

> Ella Guest, Bertie Vidgen, Alexandros Mittos, Nishanth Sastry, Gareth Tyson, and
> Helen Margetts. "An Expert Annotated Dataset for the Detection of Online Misogyny."
> *Proceedings of EACL 2021*, pages 1336–1350.
> https://aclanthology.org/2021.eacl-main.114/

Provides the primary scoring taxonomy: a three-level hierarchy of misogyny types
validated on 6,567 expert-labelled Reddit posts and comments. The four misogynistic
categories (Pejorative, Treatment, Derogation, Personal Attack) are non-mutually
exclusive and include third-level subcategories. Ground truth labels for Subtext
samples are mapped to this taxonomy.

Key finding relevant to LLM evaluation: the highest misclassification errors in
automated detection come from **implicit derogation** and **context-dependent content**
— exactly the cases where LLM outputs are most likely to be harmful yet hardest to
catch with keyword matching alone.

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
uv run inspect eval src/subtext/subtext.py
```

## Running Tests

```bash
uv run pytest
```
