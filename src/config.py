from typing import List

import yaml


class Config(yaml.YAMLObject):
    def __init__(self):
        self.meetings: List[Meeting] = []
        self.compromise = False


class Meeting:
    def __init__(self):
        self.description = None
        self.link = None
        self.id = None
        self.password = None
        self.duration = None
        self.day = None
        self.time = None


def parse_meeting(meeting_load) -> Meeting:
    meeting = Meeting()

    if 'description' in meeting_load:
        meeting.description = meeting_load['description']

    if 'id' in meeting_load:
        meeting.id = str(meeting_load['id'])

    if 'password' in meeting_load:
        meeting.password = meeting_load['password']

    if 'link' in meeting_load:
        meeting.link = meeting_load['link']

    if 'day' in meeting_load:
        meeting.day = meeting_load['day']

    if 'time' in meeting_load:
        if type(meeting_load['time']) is str:
            meeting.time = meeting_load['time']
        else:
            loaded_time = str(meeting_load['time'])
            if len(loaded_time) == 4:
                meeting.time = f'{loaded_time[:-2]}:{loaded_time[-2:]}'

    if 'duration' in meeting_load:
        meeting.duration = meeting_load['duration']

    return meeting


def parse_config(filename) -> Config:
    with open(filename) as file:
        load = yaml.safe_load(file)
        config = Config()

        if not load:
            return config

        if 'compromise' in load:
            config.compromise = load['compromise']

        if 'meetings' in load:
            for meeting_load in load['meetings']:
                config.meetings.append(parse_meeting(meeting_load))

        return config
