from enum import Enum


class ActivityType(Enum):
    FOLLOW = 'Follow'
    UNDO = 'Undo'


def get_activity_type(activity):
    return ActivityType(activity['type'])
