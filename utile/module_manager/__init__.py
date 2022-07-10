from utile.CacheManager import JSONCache
from utile.module_manager.ModulesRepo import DEFAULT_MODULES_REPO, ModulesRepo
import utile.utils
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
        
        self.repos: list[ModulesRepo] = []
        self.repos_cache = JSONCache(utile.utils.Directory.get_cache_path("repos"))
        repos_urls = self.repos_cache.read_cache("urls.json")
        if repos_urls is None:
            repos_urls = [DEFAULT_MODULES_REPO]
            self.repos_cache.write_cache("urls.json", repos_urls)
        for url in repos_urls:
            repo = ModulesRepo(url)
            self.repos.append(repo)
        print("Loading module management")
        
        if len(self.repos) == 0:
            print("No repo added. No modules will be available to download.")
        
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
    

module_manager = None

def module_manager_initer(func):
    def wrapper(*args, **kwargs):
        global module_manager
        if not module_manager:
            module_manager = ModuleManager()
        return func(*args, **kwargs)
    return wrapper


class ModuleManagerInterface:
    @module_manager_initer
    def list(self):
        print("List of installed modules:")
        for mod in module_manager.modules:
            print(mod.manifest.name + "@" + mod.manifest.version)
    
    @module_manager_initer
    def rebuild_repos_cache(self):
        print("Rebuilding cache for repos...")
        for repo in module_manager.repos:
            print("Rebuilding cache for repo {}...".format(termcolor.colored(repo.url, "green")))
            repo.rebuild_cache()
        if len(module_manager.repos) == 0:
            print("No repo")
        
    @module_manager_initer
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
