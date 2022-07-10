from webbrowser import get
import fire
import inspect
from utile.module_manager import ModuleManagerInterface
from utile.module_manager.ModulesLoader import ModulesLoader
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
        return ModuleManagerInterface


class CommandLine:
    def __init__(self) -> None:
        self.modules: list[Module] = []
        self.interface = None
        
        self.modules_cache_path = utile.utils.Directory.get_cache_path("modules.cache")
        self.loader = ModulesLoader()
        self.load_modules()
        
    def load_modules(self):
        self.interface = CommandLineInterface()
        for module in self.loader.modules:
            setattr(self.interface, module.manifest.name, self.make_module_executor(module))
    
    def make_module_executor(self, module: Module):
        def wrapper():
            return module.import_module().MODULE
        return wrapper
