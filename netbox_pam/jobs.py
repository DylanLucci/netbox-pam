from datetime import timedelta

from core.choices import JobStatusChoices
from core.models import Job


def sync_job(job: Job, *args, **kwargs):
    try:
        job.start()
        print("Running sync job...")
    except Exception as e:
        job.terminate(status=JobStatusChoices.STATUS_ERRORED, error=str(e))
    finally:
        job.terminate()
        if job.interval:
            new_scheduled_time = job.scheduled + timedelta(minutes=job.interval)
            job.enqueue(
                sync_job,
                name=job.name,
                user=job.user,
                schedule_at=new_scheduled_time,
                interval=job.interval,
            )
