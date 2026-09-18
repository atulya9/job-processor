from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .exceptions import InvalidRecordError


class Status(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    RUNNING = "running"


@dataclass
class JobRecord:
    job_id: str
    status: Status
    started_at: datetime
    finished_at: datetime | None
    attempt: int

    def __post_init__(self):
        if not self.job_id:
            raise InvalidRecordError("job_id must be non-empty")

        if self.attempt < 1:
            raise InvalidRecordError("attempt must be positive")

        if self.finished_at and self.finished_at < self.started_at:
            raise InvalidRecordError("finished_at cannot precede started_at")

        if self.status in (Status.SUCCESS, Status.FAILED) and self.finished_at is None:
            raise InvalidRecordError("completed jobs must have finished_at")

    @property
    def duration_seconds(self) -> float | None:
        if self.finished_at is None:
            return None
        return (self.finished_at - self.started_at).total_seconds()


@dataclass
class JobSummary:
    total: int
    successful: int
    failed: int
    successful_duration_average: float | None
    required_retries: int
