from .models import JobRecord, JobSummary, Status


def summarize(records: list[JobRecord]) -> JobSummary:
    successful = [record for record in records if record.status == Status.SUCCESS]

    failed = [record for record in records if record.status == Status.FAILED]

    success_durations = [
        record.duration_seconds
        for record in successful
        if record.duration_seconds is not None
    ]

    average_duration = (
        sum(success_durations) / len(success_durations) if success_durations else None
    )

    return JobSummary(
        total=len(records),
        successful=len(successful),
        failed=len(failed),
        successful_duration_average=average_duration,
        required_retries=sum(record.attempt > 1 for record in records),
    )
