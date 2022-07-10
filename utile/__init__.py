from webbrowser import get
import fire
import inspect
from utile.module_manager import ModuleManager
from utile.modules import youtube_dl, convert
import termcolor
import os
import importlib
from utile.modules.Module import Module
import colorama
from functools import cache
import json
import utile.utils

colorama.init()


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
    # Method will be used for lazy loading
    # def __getattribute__(self, __name: str):
    #     if __name.startswith("__"):
    #         return super().__getattribute__(__name)
    #     return command_line.module_getter(__name)
    def module(self):
        return ModuleManager


class CommandLine:
    def __init__(self) -> None:
        self.modules: list[Module] = []
        self.interface = None
        
        self.modules_cache_path = utile.utils.Directory.get_cache_path("modules.cache")
        
        self.load_modules()
    
    def build_modules_cache(self, files: list = None):
        print("Building modules cache...")
        with utile.utils.create_spinner():
            modules_filenames = self.get_modules_files() if not files else files
            cache_path = self.modules_cache_path
            with open(cache_path, "w") as f:
                json.dump(modules_filenames, f)
    
    @cache
    def get_modules_files(self):
        # Load from cache
        if os.path.isfile(self.modules_cache_path):
            try:
                with open(self.modules_cache_path, "r") as f:
                    filenames = json.load(f)
                return filenames
            except:
                print("Could not load modules from cache. Loading modules manually...")
        # Cache doesn't exist, we create it
        self_path = os.path.realpath(os.path.dirname(__file__))
        modules_path = os.path.join(self_path, "modules")
        files = os.listdir(modules_path)
        if "Module.py" in files:
            files.remove("Module.py")
        if "Module.pyc" in files:
            files.remove("Module.pyc")
        files = [file.removesuffix(".py").removesuffix(".pyc") for file in files if not os.path.isdir(
            os.path.join(modules_path, file)
        ) and not file == "__init__.py" and not file == "__init__.pyc"]
        self.build_modules_cache(files)
        return files
    
    def load_modules(self):
        """
        
        The module loading method will soon be changed. The modules will be cached in just one file,
        modules will be lazy loaded... Note to myself: do not create any module before
        module loading is completly done (or works pretty much)
        This needs to change to hopefully speed up the loading time
        of the CLI.
        
        """
        files = self.get_modules_files()
        names = []
        for file in files:
            module = importlib.import_module("utile.modules.{}".format(file))
            if not hasattr(module, "MODULE"):
                print(RuntimeWarning("MODULE_ERROR > MODULE object could not be found for module {}".format(file)))
            else:
                module_name = getattr(module, "MODULE").get_command_name()
                if module_name in names:
                    raise RuntimeError("Duplicate command name {}".format(module_name))
                names.append(module_name)
                module = getattr(module, "MODULE")
                self.modules.append(module)
            
        self.instantiate_modules()
                    
    def instantiate_modules(self):
        self.interface = CommandLineInterface()
        for module in self.modules:
            setattr(self.interface, module.get_command_name(), self.make_module_executor(module))
            
    def make_module_executor(self, module: Module):
        def wrapper():
            return module.get_executor()
        return wrapper
            


command_line = CommandLine()
try:
    fire.Fire(command_line.interface)
except KeyboardInterrupt:
    print(termcolor.colored("[User aborted]", "red"))
