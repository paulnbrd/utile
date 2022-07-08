import os
import sys
from yaspin import yaspin
from yaspin.spinners import Spinners
import termcolor

filepath = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))
cwd = os.getcwd()
documents_path = os.path.realpath(os.path.expanduser("~/Documents"))


class Directory:
    UTILS_DOCUMENTS_PATH = os.path.join(documents_path, "Utile CLI")
    YOUTUBE_VIDEOS = os.path.join(documents_path, "Utile CLI", "youtube")
    
    def create_storage_directory(directory_name: str):
        directory_path = os.path.join(Directory.UTILS_DOCUMENTS_PATH, directory_name)
        try:
            os.makedirs(directory_path, exist_ok=True)
        except PermissionError:
            print("Could not create data directory. Aborting.")
            sys.exit(-1)
        return directory_path
    
    def create_cache_directory(directory_name: str):
        directory_path = os.path.join(filepath, "cache", directory_name)
        try:
            os.makedirs(directory_path, exist_ok=True)
        except PermissionError:
            print("Could not create cache directory. Aborting.")
            sys.exit(-1)
        return directory_path


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
