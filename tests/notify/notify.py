import datetime

from app import scheduler
from tests.test_base import Base


class NotifyTest(Base):
    def test_add_futureTime(self):
        username: str = "test"
        password: str = "password"
        telegram_id: int = 1234567890
        content: str = "test_data"
        now = datetime.datetime.now()
        todo_time = now + datetime.timedelta(days=2)
        time = todo_time.strftime("%H:%M:%S")
        date = todo_time.strftime("%Y/%m/%d")
        todo_time_minute = (todo_time - datetime.timedelta(minutes=15)).minute

        self.register(username, username, password, telegram_id=telegram_id)
        self.login(username, password)
        self.client.post("/todo",
                         data=dict(
                             content=content,
                             time=time,
                             date=date,
                         ))

        jobs = scheduler.get_jobs()
        first_job = jobs[0]
        job_id = "1_1"

        self.assertEqual(job_id, first_job.id)
        self.assertEqual(todo_time_minute, first_job.next_run_time.minute)

    def test_add_pastTime(self):
        username: str = "test"
        password: str = "password"
        telegram_id: int = 1234567890
        content: str = "test_data"
        now = datetime.datetime.now()
        todo_time = now - datetime.timedelta(days=2)
        time = todo_time.strftime("%H:%M:%S")
        date = todo_time.strftime("%Y/%m/%d")

        self.register(username, username, password, telegram_id=telegram_id)
        self.login(username, password)
        self.client.post("/todo",
                         data=dict(
                             content=content,
                             time=time,
                             date=date,
                         ))

        jobs = scheduler.get_jobs()
        empty_jobs = []

        self.assertEqual(empty_jobs, jobs)
