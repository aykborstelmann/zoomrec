import csv
import logging
import os
import pyautogui
import schedule
import time
from datetime import datetime, timedelta

from config import parse_config, Config
from join import join
from taskmanagment import TaskManager

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

formatter = logging.Formatter("%(asctime)s %(levelname)s %(module)s - %(message)s")
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


def main():
    try:
        if DEBUG and not os.path.exists(DEBUG_PATH):
            os.makedirs(DEBUG_PATH)
    except Exception:
        logging.error("Failed to create screenshot folder!")
        raise

    config = parse_config(CONFIG_PATH)
    task_manager = TaskManager(config)

    while True:
        task_manager.run()
        time.sleep(1)


if __name__ == '__main__':
    main()
