"""
Per-vector accuracy analysis for Subtext eval logs.

Usage:
    uv run python -m subtext.analyse logs/your-run.eval
    uv run python -m subtext.analyse logs/run-a.eval logs/run-b.eval
"""

import re
import sys
from collections import defaultdict

from inspect_ai.log import read_eval_log


def _parse_sample(sample) -> tuple[str, str, float, float, float] | None:
    score = sample.scores.get("subtext_scorer")
    if not score or not isinstance(score.value, dict):
        return None
    expl = score.explanation or ""
    ans_match = re.search(r"answer='([^']+)'", expl)
    tgt_match = re.search(r"target='([^']+)'", expl)
    if not tgt_match:
        return None
    target = tgt_match.group(1)
    predicted = ans_match.group(1) if ans_match else "?"
    binary = score.value.get("binary", 0.0)
    category = score.value.get("category", 0.0)
    vector = score.value.get("vector", 0.0)
    return target, predicted, binary, category, vector


def vector_accuracy(log_path: str) -> None:
    log = read_eval_log(log_path)
    results: dict[str, dict] = defaultdict(
        lambda: {"binary": 0.0, "category": 0.0, "vector": 0.0, "wrong_as": defaultdict(int), "total": 0}
    )

    for sample in log.samples or []:
        parsed = _parse_sample(sample)
        if not parsed:
            continue
        target, predicted, binary, category, vector = parsed
        d = results[target]
        d["total"] += 1
        d["binary"] += binary
        d["category"] += category
        d["vector"] += vector
        if vector < 1.0:
            d["wrong_as"][predicted] += 1

    print(f"\n{log.eval.model} — per-vector accuracy (n={len(log.samples)})\n")
    print(f"{'Vector':<55} {'bin':>5} {'cat':>5} {'vec':>5}  {'n':<5} Misclassified as")
    print("-" * 120)
    for vec, d in sorted(results.items(), key=lambda x: x[1]["vector"] / x[1]["total"]):
        n = d["total"]
        wrong = ", ".join(
            f"{k}({v})"
            for k, v in sorted(d["wrong_as"].items(), key=lambda x: -x[1])
        )
        print(
            f"{vec:<55} {d['binary']/n:>4.0%} {d['category']/n:>5.0%} {d['vector']/n:>5.0%}  {n:<5} {wrong}"
        )


def compare(log_paths: list[str]) -> None:
    rows: dict[str, dict[str, dict]] = defaultdict(dict)
    models = []

    for path in log_paths:
        log = read_eval_log(path)
        model = log.eval.model
        models.append(model)
        for sample in log.samples or []:
            parsed = _parse_sample(sample)
            if not parsed:
                continue
            target, _, binary, category, vector = parsed
            entry = rows[target].setdefault(model, {"binary": 0.0, "category": 0.0, "vector": 0.0, "total": 0})
            entry["total"] += 1
            entry["binary"] += binary
            entry["category"] += category
            entry["vector"] += vector

    short = [m.split("/")[-1] for m in models]
    col_w = 20
    header = f"{'Vector':<55}" + "".join(f"{m:>{col_w}}" for m in short)
    print("\n" + header)
    print("-" * (55 + col_w * len(models)))

    for vec in sorted(rows.keys()):
        row = f"{vec:<55}"
        for model in models:
            d = rows[vec].get(model)
            if d and d["total"]:
                n = d["total"]
                row += f"  {d['binary']/n:.0%}/{d['category']/n:.0%}/{d['vector']/n:.0%}".rjust(col_w)
            else:
                row += f"{'—':>{col_w}}"
        print(row)

    print("\n(columns: binary/category/vector accuracy)")


def main() -> None:
    paths = sys.argv[1:]
    if not paths:
        print(__doc__)
        sys.exit(1)
    if len(paths) == 1:
        vector_accuracy(paths[0])
    else:
        compare(paths)


if __name__ == "__main__":
    main()
