# job-processor

Reads a JSON file of job execution records and prints a summary: totals, successes, failures, average successful duration, and jobs that needed retries.

## Run

```bash
uv run job-processor tests/fixtures/jobs.json
```

Malformed records are skipped with a `WARNING`. A missing file, invalid JSON, or a non-list root prints an `ERROR` and exits with status 1.

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
