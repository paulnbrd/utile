import os
import sys
from yaspin import yaspin
from yaspin.spinners import Spinners
import termcolor

filepath = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))
cache_dir = os.path.join(filepath, "cache")
modules_dir = os.path.join(filepath, "modules")
cwd = os.getcwd()
documents_path = os.path.realpath(os.path.expanduser("~/Documents"))    


def filename_friendly(string: str):
    return "".join([c for c in string if c.isalpha() or c.isdigit() or c==' ']).rstrip()


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
        directory_path = os.path.join(cache_dir, directory_name)
        try:
            os.makedirs(directory_path, exist_ok=True)
        except PermissionError:
            print("Could not create cache directory. Aborting.")
            sys.exit(-1)
        return directory_path
    
    def get_cache_path(*args):
        """Returns a cache path, but does not ensure that the directories exists
        """
        return os.path.join(cache_dir, *args)


try:
    os.makedirs(cache_dir, exist_ok=True)
except PermissionError:
    print(termcolor.colored(
        "Could not create cache directory. Please check program permissions.", "red"))
    sys.exit(-1)
try:
    os.makedirs(modules_dir, exist_ok=True)
except PermissionError:
    print(termcolor.colored(
        "Could not create modules directory. Please check program permissions.", "red"))
    sys.exit(-1)
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
