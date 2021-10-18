import csv
import logging
import os
import pyautogui
import schedule
import time
from datetime import datetime, timedelta

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
CSV_PATH = os.path.join(BASE_PATH, "meetings.csv")
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

ONGOING_MEETING = False
VIDEO_PANEL_HIDED = False


def setup_schedule():
    with open(CSV_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=CSV_DELIMITER)
        line_count = 0
        for row in csv_reader:
            if str(row["record"]) == 'true':
                start_time = (datetime.strptime(row["time"], '%H:%M') - timedelta(minutes=1)).strftime('%H:%M')
                getattr(schedule.every(), row["weekday"]) \
                    .at(start_time) \
                    .do(join, meet_id=row["id"], meet_pw=row["password"], duration=str(int(row["duration"]) * 60),
                        description=row["description"])

                line_count += 1
        logging.info("Added %s meetings to schedule." % line_count)


def join_ongoing_meeting():
    with open(CSV_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=CSV_DELIMITER)
        for row in csv_reader:
            # Check and join ongoing meeting
            curr_date = datetime.now()

            # Monday, tuesday, ..
            if row["weekday"].lower() == curr_date.strftime('%A').lower():
                curr_time = curr_date.time()

                start_time_csv = datetime.strptime(row["time"], '%H:%M')
                start_date = curr_date.replace(
                    hour=start_time_csv.hour, minute=start_time_csv.minute)
                start_time = start_date.time()

                end_date = start_date + \
                           timedelta(seconds=int(row["duration"]) * 60 + 300)  # Add 5 minutes
                end_time = end_date.time()

                recent_duration = (end_date - curr_date).total_seconds()

                if start_time < end_time:
                    if start_time <= curr_time <= end_time and str(row["record"]) == 'true':
                        logging.info(
                            "Join meeting that is currently running..")
                        join(meet_id=row["id"], meet_pw=row["password"],
                             duration=recent_duration, description=row["description"])
                else:  # crosses midnight
                    if curr_time >= start_time or curr_time <= end_time and str(row["record"]) == 'true':
                        logging.info(
                            "Join meeting that is currently running..")
                        join(meet_id=row["id"], meet_pw=row["password"],
                             duration=recent_duration, description=row["description"])


def main():
    try:
        if DEBUG and not os.path.exists(DEBUG_PATH):
            os.makedirs(DEBUG_PATH)
    except Exception:
        logging.error("Failed to create screenshot folder!")
        raise

    setup_schedule()
    join_ongoing_meeting()


if __name__ == '__main__':
    main()

while True:
    schedule.run_pending()
    time.sleep(1)
    time_of_next_run = schedule.next_run()
    time_now = datetime.now()
    remaining = time_of_next_run - time_now
    print(f"Next meeting in {remaining}", end="\r", flush=True)
