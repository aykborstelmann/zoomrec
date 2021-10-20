import datetime
import logging
from unittest import TestCase

import schedule

from config import Config, Meeting
from taskmanagment import TaskManager, JoinMeetingJob, CompressJob

logging.basicConfig(level=logging.DEBUG)


class TestTaskManager(TestCase):
    def test_init(self):
        config = Config()

        meeting = Meeting()
        meeting.time = "18:00"
        meeting.day = "monday"

        config.meetings.append(meeting)

        manager = TaskManager(config)

        jobs = manager.scheduler.get_jobs()
        self.assertEqual(1, len(jobs))
        self.assertEqual("monday", jobs[0].start_day)
        self.assertEqual(datetime.time(17, 59), jobs[0].at_time)


    def test_enqueue(self):
        config = Config()

        meeting = Meeting()
        meeting.time = "18:00"
        meeting.day = "monday"

        config.meetings.append(meeting)

        manager = TaskManager(config)
        manager.scheduler.run_all()

        self.assertEqual(1, len(manager.queue))
        self.assertEqual(JoinMeetingJob, type(manager.queue[0]))


    def test_compress(self):
        config = Config()
        config.compress = True

        meeting = Meeting()
        meeting.time = "18:00"
        meeting.day = "monday"

        config.meetings.append(meeting)

        manager = TaskManager(config)
        manager.scheduler.run_all()

        self.assertEqual(1, len(manager.queue))
        self.assertEqual(JoinMeetingJob, type(manager.queue[0]))
        manager.queue[0].run = lambda: "output.mkv"

        manager.run()

        self.assertEqual(1, len(manager.queue))
        self.assertEqual(CompressJob, type(manager.queue[0]))
        manager.queue[0].run = lambda: "done"

        manager.run()
        self.assertEqual(0, len(manager.queue))
