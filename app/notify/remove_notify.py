from app import scheduler


def remove_notify(job_id: str) -> bool:
    job = scheduler.get_job(job_id)
    if job:
        scheduler.remove_job(job.id)
        return True
    return False
