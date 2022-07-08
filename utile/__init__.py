import fire
import inspect
from utile.modules import youtube_dl, convert
import termcolor
import os
import importlib

from utile.modules.Module import Module


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


class CommandLineInterface:
    pass


class CommandLine:
    def __init__(self) -> None:
        self.modules: list[Module] = []
        self.interface = None
        
        self.load_modules()
        
    def load_modules(self):
        self_path = os.path.realpath(os.path.dirname(__file__))
        modules_path = os.path.join(self_path, "modules")
        files = os.listdir(modules_path)
        if "Module.py" in files:
            files.remove("Module.py")
        files = [file.removesuffix(".py") for file in files if not os.path.isdir(
            os.path.join(modules_path, file)
        )]
        
        for file in files:
            module = importlib.import_module("cli.modules.{}".format(file))
            if not hasattr(module, "MODULE"):
                raise RuntimeError("MODULE object could not be found for module {}".format(file))
            self.modules.append(getattr(module, "MODULE"))
            
        self.instantiate_modules()
                    
    def instantiate_modules(self):
        self.interface = CommandLineInterface()
        for module in self.modules:
            setattr(self.interface, module.get_command_name(), module.get_executor())
            


try:
    fire.Fire(CommandLine().interface)
except KeyboardInterrupt:
    print(termcolor.colored("[User aborted]", "red"))
