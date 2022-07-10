from .manifest import Manifest
from .packager import package, unpackage
from .Module import Module
import termcolor
import os
import base64
import sys


class ModuleManager:
    
    def generate_nonce(self):
        module_id = "m" + base64.b64encode(os.urandom(8)).hex()
        while module_id in self.module_ids:
            module_id = self.generate_nonce()
        return module_id
    
    def __init__(self, auto_discover_modules: bool = True) -> None:
        self.modules: list[Module] = []
        self.module_ids: list[str] = []
        
        root_path = os.path.realpath(
            os.path.dirname(
                sys.argv[0]
            )
        )
        self.modules_path = os.path.join(root_path, "modules")
        
        self.module_ids = [d for d in os.listdir(self.modules_path) if d.startswith("m") and os.path.isdir(
            os.path.join(self.modules_path, d)
        )]
        
        if auto_discover_modules:
            self.discover_modules()
        
    def discover_modules(self):
        for module_id in self.module_ids:
            module = Module(module_id)
            self.modules.append(module)
            
    def get_module_names(self):
        return [mod.manifest.name for mod in self.modules]
    

module_manager = ModuleManager()


class ModuleManagerInterface:
    def list(self):
        print("List of installed modules:")
        for mod in module_manager.modules:
            print(mod.manifest.name + "@" + mod.manifest.version)
        
    def install(self, module: str, update: bool = False):
        module = str(module)
        splitted = module.split("@")
        if len(splitted) == 2:
            module_name, version = splitted
        elif len(splitted) > 2:
            print(termcolor.colored("Invalid module name", "red"))
            return
        else:
            module_name, version = module, "latest"
        print("Searching for module {}@{}...".format(
            termcolor.colored(module_name, "green"),
            termcolor.colored(version, "blue")
        ))
        if not update and module_name in module_manager.get_module_names():
            print(termcolor.colored("Module already installed", "green"))
