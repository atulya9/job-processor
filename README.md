# job-processor

Reads a JSON file of job execution records and prints a summary: totals, successes, failures, average successful duration, and jobs that needed retries.

## How it works

The CLI loads the file, the parser turns each object into a `JobRecord` (or a warning), and the processor counts the valid records and prints the summary. File-level problems (missing file, invalid JSON, non-list root) print an `ERROR` and exit with status 1. Malformed records are skipped with a `WARNING`.

## Run

```bash
uv sync
uv run job-processor tests/fixtures/jobs.json
```

## Tests

```bash
uv run pytest
```

## Assumptions

- Input is a JSON array of objects with `job_id`, `status`, `started_at`, `finished_at`, and `attempt`.
- `status` is one of `success`, `failed`, or `running`.
- Timestamps are ISO-8601 (`datetime.fromisoformat`).
- `finished_at` may be `null` for running jobs; completed jobs must have it, and it cannot precede `started_at`.
- `attempt` is a positive integer. A job required retries if `attempt > 1`.
- Summary totals count only valid records. Running jobs are in the total but are neither successful nor failed.
- Average successful duration is in seconds, or `n/a` when there are no successful jobs.

## Improvements

- The whole JSON file is loaded into memory.
- `summarize` walks the records more than once.
- Per-record warnings go to stdout, not stderr.
- `job_id` is not type-checked.
- Tests do not cover the CLI.
