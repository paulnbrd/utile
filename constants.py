import os
import sys
from yaspin import yaspin
from yaspin.spinners import Spinners

filepath = os.path.realpath(os.path.dirname(__file__))


class Directory:
    YOUTUBE_VIDEOS = os.path.join(filepath, "youtube")


os.makedirs(Directory.YOUTUBE_VIDEOS, exist_ok=True)


def create_spinner():
    return yaspin(Spinners.timeTravel)
