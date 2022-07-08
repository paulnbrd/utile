import os
import sys
from yaspin import yaspin
from yaspin.spinners import Spinners
import termcolor

filepath = os.path.realpath(os.path.dirname(__file__))
cwd = os.getcwd()
documents_path = os.path.realpath(os.path.expanduser("~/Documents"))


class Directory:
    UTILS_DOCUMENTS_PATH = os.path.join(documents_path, "CLI_UTILS")
    YOUTUBE_VIDEOS = os.path.join(documents_path, "CLI_UTILS", "youtube")
    
    def create_storage_directory(self, directory_name: str):
        directory_path = os.path.join(Directory.UTILS_DOCUMENTS_PATH, directory_name)
        Directory.__setattr__(directory_name.upper(), directory_path)
        return directory_name.upper()


try:
    os.makedirs(Directory.YOUTUBE_VIDEOS, exist_ok=True)
except PermissionError:
    print(termcolor.colored(
        "Could not create data directory. Please check program permissions.", "red"))
    sys.exit(-1)


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
