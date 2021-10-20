from typing import List

import yaml


class Config(yaml.YAMLObject):
    def __init__(self):
        self.meetings: List[Meeting] = []
        self.compress = False


class Meeting:
    def __init__(self):
        self.description: str = None
        self.link: str = None
        self.id: str = None
        self.password: str = None
        self.duration: int = None
        self.day: str = None
        self.time: str = None


def parse_meeting(meeting_load) -> Meeting:
    meeting = Meeting()

    if 'description' in meeting_load:
        meeting.description = meeting_load['description']

    if 'id' in meeting_load:
        meeting.id = str(meeting_load['id'])

    if 'password' in meeting_load:
        meeting.password = str(meeting_load['password'])

    if 'link' in meeting_load:
        meeting.link = meeting_load['link']
        meeting.id = meeting_load['link']

    if 'day' in meeting_load:
        meeting.day = meeting_load['day']

    if 'time' in meeting_load:
        if type(meeting_load['time']) is str:
            meeting.time = meeting_load['time']

    if 'duration' in meeting_load:
        meeting.duration = meeting_load['duration']

    return meeting


def parse_config(filename) -> Config:
    with open(filename) as file:
        load = yaml.safe_load(file)
        config = Config()

        if not load:
            return config

        if 'compress' in load:
            config.compress = load['compress']

        if 'meetings' in load:
            for meeting_load in load['meetings']:
                config.meetings.append(parse_meeting(meeting_load))

        return config
