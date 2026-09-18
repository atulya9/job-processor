from pathlib import Path

import pytest

from job_processor.exceptions import InvalidRecordError
from job_processor.models import Status
from job_processor.parser import load_records, parse_record
from job_processor.processor import summarize

FIXTURE = Path(__file__).parent / "fixtures" / "jobs.json"

VALID = {
    "job_id": "job-001",
    "status": "success",
    "started_at": "2026-09-18T09:00:00Z",
    "finished_at": "2026-09-18T09:02:30Z",
    "attempt": 1,
}


def test_parse_record_computes_duration():
    record = parse_record(VALID)
    assert record.status == Status.SUCCESS
    assert record.duration_seconds == 150.0


def test_parse_record_rejects_malformed():
    missing_status = {key: value for key, value in VALID.items() if key != "status"}
    with pytest.raises(InvalidRecordError, match="missing field 'status'"):
        parse_record(missing_status)

    with pytest.raises(InvalidRecordError, match="invalid attempt: 'two'"):
        parse_record({**VALID, "attempt": "two"})


def test_load_records_skips_malformed():
    records, errors = load_records(FIXTURE)
    assert [record.job_id for record in records] == [
        "job-001",
        "job-002",
        "job-003",
        "job-004",
        "job-005",
        "job-006",
        "job-007",
    ]
    assert len(errors) == 7


def test_summarize_counts_average_and_retries():
    records, _ = load_records(FIXTURE)
    summary = summarize(records)
    assert summary.total == 7
    assert summary.successful == 4
    assert summary.failed == 2
    assert summary.successful_duration_average == 116.25
    assert summary.required_retries == 2


def test_summarize_average_is_none_without_successes():
    failed = parse_record(
        {
            "job_id": "job-004",
            "status": "failed",
            "started_at": "2026-09-18T09:15:00Z",
            "finished_at": "2026-09-18T09:15:45Z",
            "attempt": 1,
        }
    )
    assert summarize([failed]).successful_duration_average is None
    assert summarize([]).successful_duration_average is None
