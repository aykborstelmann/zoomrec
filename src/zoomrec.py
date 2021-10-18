import csv
import logging
import os
import pyautogui
import schedule
import time
from datetime import datetime, timedelta

from config import parse_config, Config
from join import join

global ONGOING_MEETING
global VIDEO_PANEL_HIDED

# Turn DEBUG on:
#   - screenshot on error
#   - record joining
#   - do not exit container on error
DEBUG = True if os.getenv('DEBUG') == 'True' else False

# Get vars
BASE_PATH = os.getenv('HOME')
CONFIG_PATH = os.path.join(BASE_PATH, "config.yml")
IMG_PATH = os.path.join(BASE_PATH, "img")
REC_PATH = os.path.join(BASE_PATH, "recordings")
DEBUG_PATH = os.path.join(REC_PATH, "screenshots")

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
root_logger.addHandler(stream_handler)

file_handler = logging.FileHandler(f'{REC_PATH}/output.log')
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

NAME_LIST = [
    'iPhone',
    'iPad',
    'Macbook',
    'Desktop',
    'Huawei',
    'Mobile',
    'PC',
    'Windows',
    'Home',
    'MyPC',
    'Computer',
    'Android'
]

TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
CSV_DELIMITER = ';'


def setup_schedule(config: Config):
    for meeting in config.meetings:
        start_time = (datetime.strptime(meeting.time, '%H:%M') - timedelta(minutes=1)).strftime('%H:%M')
        getattr(schedule.every(), meeting.day) \
            .at(start_time) \
            .do(join, meeting)

    logging.info("Added %s meetings to schedule." % len(config.meetings))


def join_ongoing_meeting(config: Config):
    for meeting in config.meetings:

        # Check and join ongoing meeting
        curr_date = datetime.now()

        # Monday, tuesday, ..
        if meeting.day.lower() == curr_date.strftime('%A').lower():
            curr_time = curr_date.time()

            start_time_csv = datetime.strptime(meeting.time, '%H:%M')
            start_date = curr_date.replace(
                hour=start_time_csv.hour, minute=start_time_csv.minute)
            start_time = start_date.time()

            end_date = start_date + timedelta(seconds=int(meeting.duration) * 60 + 300)  # Add 5 minutes
            end_time = end_date.time()

            recent_duration = (end_date - curr_date).total_seconds()

            if start_time < end_time:
                if start_time <= curr_time <= end_time:
                    logging.info(
                        "Join meeting that is currently running..")
                    join(meeting)
            else:  # crosses midnight
                if curr_time >= start_time or curr_time <= end_time:
                    logging.info(
                        "Join meeting that is currently running..")
                    join(meeting)


def main():
    try:
        if DEBUG and not os.path.exists(DEBUG_PATH):
            os.makedirs(DEBUG_PATH)
    except Exception:
        logging.error("Failed to create screenshot folder!")
        raise

    config = parse_config(CONFIG_PATH)

    setup_schedule(config)
    join_ongoing_meeting(config)


if __name__ == '__main__':
    main()

while True:
    schedule.run_pending()
    time.sleep(1)
    time_of_next_run = schedule.next_run()
    time_now = datetime.now()
    remaining = time_of_next_run - time_now
    print(f"Next meeting in {remaining}", end="\r", flush=True)
