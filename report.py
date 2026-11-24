"""Build an HTML report from sample simulation test results."""

import csv
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent


def summarize(results):
    """Return counts for a list of rows with PASS or FAIL as the status."""
    passed = 0
    for result in results:
        status = result["status"]
        if status not in ("PASS", "FAIL"):
            raise ValueError(f"Unknown test status: {status}")
        if status == "PASS":
            passed += 1
    return {"total": len(results), "passed": passed, "failed": len(results) - passed}


def build_report(output_path, source_path=ROOT / "results.csv"):
    with source_path.open(encoding="utf-8", newline="") as source:
        results = list(csv.DictReader(source))

    counts = summarize(results)
    rows = []
    for result in results:
        name = escape(result["scenario"])
        status = result["status"]
        rows.append(
            f'<tr><th scope="row">{name}</th>'
            f'<td><span class="{status.lower()}">{status}</span></td></tr>'
        )

    template = Template((ROOT / "template.html").read_text(encoding="utf-8"))
    page = template.substitute(rows="\n".join(rows), **counts)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    build_report(ROOT / "site" / "index.html")
    print("Built site/index.html")
