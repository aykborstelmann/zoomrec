from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import logging
from types import FunctionType
from typing import List, Optional

from schedule import Scheduler

from config import Config, Meeting
from join import join


class Job(ABC):
    def __init__(self):
        self.successful = False
        self.done = False
        self.on_success: Optional[FunctionType] = None

    def start(self):
        result = self.run()
        self.done = True
        if result:
            self.successful = True
            if self.on_success and type(self.on_success) == FunctionType:
                self.on_success(result)

    @abstractmethod
    def run(self):
        pass


class JoinMeetingJob(Job):
    def __init__(self, meeting: Meeting, seconds_remaining=None):
        super().__init__()
        self.meeting = meeting
        self.seconds_remaining = seconds_remaining if seconds_remaining else self.meeting.duration

    def run(self):
        join(self.meeting, self.seconds_remaining)


class CompressJob(Job):
    def __init__(self, filename):
        super().__init__()

    def run(self):
        pass


class TaskManager:
    log = logging.getLogger("TaskManager")

    def __init__(self, config: Config):
        self.scheduler = Scheduler()
        self.config = config
        self.queue: List[Job] = []

        for meeting in config.meetings:
            self.append_meeting_if_running(meeting)

            start_time = (datetime.strptime(meeting.time, '%H:%M') - timedelta(minutes=1)).strftime('%H:%M')
            getattr(self.scheduler.every(), meeting.day) \
                .at(start_time) \
                .do(self.enqueue_meeting_and_follow_up, meeting)
        self.log.info(f"Setup {len(config.meetings)} meeting/s")

    def append_meeting_if_running(self, meeting):
        current_date = datetime.now()
        meeting_is_today = meeting.day.lower() == current_date.strftime('%A').lower()
        if meeting_is_today:
            start_time_from_config = datetime.strptime(meeting.time, '%H:%M')
            start_date = current_date.replace(hour=start_time_from_config.hour, minute=start_time_from_config.minute)

            end_date = start_date + timedelta(seconds=int(meeting.duration) * 60)  # Add 5 minutes
            seconds_remaining = (end_date - current_date).total_seconds()

            meeting_is_running = start_date <= current_date <= end_date
            if meeting_is_running:
                logging.info("Join meeting that is currently running..")

                self.queue.append(JoinMeetingJob(meeting, seconds_remaining))

    def enqueue_meeting_and_follow_up(self, meeting):
        join_meeting_job = JoinMeetingJob(meeting)

        if self.config.compress:
            def on_success(filename):
                self.queue.append(CompressJob(filename))

            join_meeting_job.on_success = on_success

        self.queue.append(join_meeting_job)
        self.log.info("Enqueue join meeting job")

    def run(self):
        self.scheduler.run_pending()
        if len(self.queue) > 0:
            self.log.debug("Queue not empty, executing first job")
            job = self.queue.pop()
            job.start()
        else:
            time_of_next_run = self.scheduler.next_run
            time_now = datetime.now()
            remaining = time_of_next_run - time_now
            print(f"Next meeting in {remaining}", end="\r", flush=True)
