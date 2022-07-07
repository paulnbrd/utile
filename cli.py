import fire
import inspect
from modules import youtube_dl, convert


def static_class(*args, **kwargs) -> callable:
    """Decorator to transform a class into a static object (instatiate the class).
    Arguments can be provided to the decorator, and will be passed telquel
    to the class constructor.
    """
    if len(args) == 1 and inspect.isclass(args[0]):
        # The first argument is a class, the static class we want
        return args[0]()
    # The first argument is not a class,
    # Used as decorator with parameters

    def wrapper(cl) -> object:
        # Instantiate the class with the provided arguments
        return cl(*args, **kwargs)
    return wrapper


@static_class
class API:
    def youtube_download(self, urls: list[str], audio_only: bool = False):
        youtube_dl.execute(urls, audio_only=audio_only)


class CommandLine:
    def youtube(self, *urls: str, onlyaudio: bool = False):
        # start_time = time.time()
        API.youtube_download(urls, onlyaudio)
        # end_time = time.time()
        # return "Finished in {}s".format(round(end_time - start_time, 2))

    def convert(self, image_path: str, format: str = "png", width: int = None, height: int = None):
        convert.execute(image_path, format, width, height)


if __name__ == "__main__":
    try:
        fire.Fire(CommandLine)
    except KeyboardInterrupt:
        print("User aborted")
