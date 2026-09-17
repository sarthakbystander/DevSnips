#!/usr/bin/env python3
"""
Bundle a benchmark run + its aggregate report into a single JSON payload,
then inline it into the viewer.html template (or assets/eval_review.html)
to produce a standalone, shareable review page — no server needed to open
it, just double-click.

Usage:
    python3 generate_review.py --run ../scripts_out/benchmark.json \\
        --report ../scripts_out/report.json \\
        --template viewer.html \\
        --out ../scripts_out/eval_review.html
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from utils import load_json  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--template", default=os.path.join(os.path.dirname(__file__), "viewer.html"))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    run = load_json(args.run)
    report = load_json(args.report)

    payload = {"run": run, "report": report}
    payload_json = json.dumps(payload)

    with open(args.template, "r", encoding="utf-8") as f:
        template = f.read()

    marker = "/*__EVAL_DATA__*/"
    if marker not in template:
        print(f"ERROR: template {args.template} is missing the {marker} injection marker")
        raise SystemExit(1)

    out_html = template.replace(marker, f"const EVAL_DATA = {payload_json};")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out_html)

    print(f"wrote standalone review page: {args.out}")


if __name__ == "__main__":
    main()
