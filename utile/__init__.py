from utile.module_manager import ModuleManagerInterface
from utile.module_manager.Module import Module
from utile.module_manager.ModulesLoader import ModulesLoader
import colorama
import utile.utils

colorama.init()

module_loader = ModulesLoader()

class CommandLineInterface:
    def module(self):
        return ModuleManagerInterface


class CommandLine:
    def __init__(self) -> None:
        self.modules: list[Module] = []
        self.interface = None
        
        self.modules_cache_path = utile.utils.Directory.get_cache_path("modules.cache")
        self.loader = module_loader
        self.load_modules()
        
    def load_modules(self):
        self.interface = CommandLineInterface()
        for module in self.loader.modules:
            setattr(self.interface, module.manifest.name, self.make_module_executor(module))
    
    def make_module_executor(self, module: Module):
        def wrapper():
            return module.import_module().MODULE  # We lazy load there
        return wrapper
