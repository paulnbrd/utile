import os
import sys
from yaspin import yaspin
from yaspin.spinners import Spinners

filepath = os.path.realpath(os.path.dirname(__file__))
cwd = os.cwd()
documents_path = os.path.realpath(os.path.expanduser("~/Documents"))


class Directory:
    YOUTUBE_VIDEOS = os.path.join(filepath, "youtube")


os.makedirs(Directory.YOUTUBE_VIDEOS, exist_ok=True)


class StandardContext:

    @property
    def text(self):
        return ""

    @text.setter
    def text(self, text: str):
        print(text, end="")

    def __enter__(self, *args, **kwargs):
        pass
        return self

    def __exit__(self, *args, **kwargs):
        pass


def create_spinner():
    if not sys.stdin.isatty():
        return StandardContext()
    return yaspin(Spinners.timeTravel)
