import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .exceptions import InvalidRecordError
from .models import JobRecord, Status


def _require(record: dict[str, Any], field: str) -> Any:
    if field not in record:
        raise InvalidRecordError(f"missing field {field!r}")
    return record[field]


def _parse_attempt(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidRecordError(f"invalid attempt: {value!r}")
    return value


def parse_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise InvalidRecordError(f"Invalid datetime: {value!r}") from exc


def parse_record(record: dict[str, Any]) -> JobRecord:
    try:
        return JobRecord(
            job_id=_require(record, "job_id"),
            status=Status(_require(record, "status")),
            started_at=parse_datetime(_require(record, "started_at")),
            finished_at=(
                parse_datetime(record["finished_at"])
                if record.get("finished_at")
                else None
            ),
            attempt=_parse_attempt(_require(record, "attempt")),
        )
    except (ValueError, TypeError) as exc:
        raise InvalidRecordError(str(exc)) from exc


def load_records(path: Path) -> tuple[list[JobRecord], list[str]]:
    with open(path) as w:
        data = json.load(w)

    if not isinstance(data, list):
        raise TypeError("The input JSON is invalid. Expected a list")

    records = []
    errors = []

    for index, record in enumerate(data):
        try:
            if not isinstance(record, dict):
                raise InvalidRecordError("Record must be an object")

            records.append(parse_record(record))
        except InvalidRecordError as exc:
            errors.append(f"record {index}: {exc}")

    return records, errors
