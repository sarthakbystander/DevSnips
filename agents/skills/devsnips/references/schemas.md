# Eval schemas

Shared shapes used by `scripts/run_eval.py`, `agents/analyzer.md`,
`agents/grader.md`, `agents/comparator.md`, and `eval-viewer/`.

## Scenario (input to run_eval.py)

```json
{
  "id": "react-ts-modal",
  "prompt": "Add a confirmation dialog before deleting a project from the settings page.",
  "project_context": {
    "stack": "React + TypeScript",
    "styling": "Tailwind CSS",
    "notes": "Existing components live in src/components/, use PascalCase filenames."
  },
  "expected": {
    "resource_type": "component",
    "family_hint": "Dialogs",
    "tech_hint": "React",
    "must_use_tsx": true
  },
  "tags": ["react", "dialog", "typescript"]
}
```

`expected` is a loose hint set for the grader/analyzer to check against —
not a strict path the agent must match verbatim (a close-match Dialogs
variant is fine; picking a Dropdown family is not).

## Analyzer output

See the structured-JSON shape defined in `agents/analyzer.md` directly (one
key per SKILL.md phase, each `{evidence, notes}`).

## Grader output

```json
{
  "scenario_id": "react-ts-modal",
  "scores": { "1": 2, "2": 2, "...": "...", "12": 1 },
  "percent": 87.5,
  "hard_failure": false,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "verdict": "pass"
}
```

## Benchmark run (output of run_loop.py, input to aggregate_benchmark.py)

```json
{
  "run_id": "2026-09-16T12:00:00Z",
  "skill_version": "1.0.1",
  "results": [ /* array of grader outputs, one per scenario */ ]
}
```

## Aggregate report (output of aggregate_benchmark.py / generate_report.py)

```json
{
  "run_id": "...",
  "n_scenarios": 12,
  "pass_rate": 0.75,
  "mean_percent": 81.2,
  "hard_failures": 1,
  "criterion_means": { "1": 1.9, "2": 1.6, "...": "..." },
  "worst_criteria": [2, 9],
  "worst_scenarios": ["react-ts-modal"]
}
```

`worst_criteria` = the criteria with the lowest mean score across the run —
this is what `improve_description.py` targets first, since a low mean on one
criterion across many scenarios usually means a SKILL.md wording gap rather
than a one-off mistake.
