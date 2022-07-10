from utile.module_manager.packager import unpackage
from .manifest import Manifest
import importlib
import os
import sys


class ModuleError:
    def __init__(self, message: str) -> None:
        self.message = message


class Module:
    def __init__(self, id: str, manifest: Manifest = None, manifest_auto_load: bool = True) -> None:
        self.manifest: Manifest = manifest
        self.module_id = id
        self.imported = None
        
        root_path = os.path.realpath(
            os.path.dirname(
                sys.argv[0]
            )
        )
        self.modules_path = os.path.join(root_path, "modules")
        self.module_dir = os.path.join(self.modules_path, self.module_id)
        
        if manifest_auto_load and manifest is None:
            if not self.is_installed():
                raise ModuleError("Module is not installed but manifest_auto_load is True")
            with open(os.path.join(self.module_dir, "manifest.json")) as f:
                data = f.read()
            manifest = Manifest(data)
            self.manifest = manifest
        
    def is_installed(self):
        # Checks if the directory and required files are present
        # If not, it means that it is a module not installed.
        if not os.path.isdir(self.module_dir):
            return False
        if not os.path.isfile(os.path.join(self.module_dir, "module.py")) \
            and not os.path.isfile(os.path.join(self.module_dir, "module.pyc")):
            return False
        if not os.path.isfile(os.path.join(self.module_dir, "manifest.json")):
            return False
        return True
        
    def import_module(self):
        self.imported = importlib.import_module("modules.{}.module".format(self.module_id))
        return self.imported
        
    def install(self, packaged):
        if self.is_installed():
            return True
        try:
            unpackage(packaged, self.module_dir)
            return True
        except Exception as e:
            print("Error while installing module ({})".format(e))
            return False
