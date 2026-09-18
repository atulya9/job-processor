import argparse
import json
import sys
from pathlib import Path

from .models import JobSummary
from .parser import load_records
from .processor import summarize


def print_job_summary(summary: JobSummary) -> None:
    average = summary.successful_duration_average
    average_text = "n/a" if average is None else f"{average:.2f}"
    rows = [
        ("Total jobs", summary.total),
        ("Successful jobs", summary.successful),
        ("Failed jobs", summary.failed),
        ("Average successful job duration", average_text),
        ("Jobs that required retries", summary.required_retries),
    ]
    width = max(len(label) for label, _ in rows)

    print("\nJob Summary\n-----------")
    for label, value in rows:
        print(f"{label:<{width + 1}}  {value}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    try:
        records, errors = load_records(args.path)
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)
    except TypeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    for error in errors:
        print(f"WARNING: {error}")

    summary = summarize(records)

    print_job_summary(summary)
