from webbrowser import get
import fire
import inspect
from utile.modules import youtube_dl, convert
import termcolor
import os
import importlib
from utile.modules.Module import Module
import colorama

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
        if "Module.pyc" in files:
            files.remove("Module.pyc")
        files = [file.removesuffix(".py").removesuffix(".pyc") for file in files if not os.path.isdir(
            os.path.join(modules_path, file)
        ) and not file == "__init__.py" and not file == "__init__.pyc"]
        
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
                if not hasattr(module, "init_module"):
                    print("[{}] It is highly recommended to have an init_module method on your module to speed up the CLI loading time".format(module.get_command_name()))
                self.modules.append(module)
            
        self.instantiate_modules()
                    
    def instantiate_modules(self):
        self.interface = CommandLineInterface()
        for module in self.modules:
            setattr(self.interface, module.get_command_name(), self.make_module_executor(module))
            
    def make_module_executor(self, module: Module):
        def wrapper():
            # We initialize module
            if hasattr(module, "init_module"):
                getattr(module, "init_module")()
            return module.get_executor()
        return wrapper
            


try:
    fire.Fire(CommandLine().interface)
except KeyboardInterrupt:
    print(termcolor.colored("[User aborted]", "red"))
