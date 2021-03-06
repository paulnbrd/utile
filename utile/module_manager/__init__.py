import shutil
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
            if not repo.is_valid_repo():
                print(repo.url, "does not seem to be a valid repo. It can also be a network problem.")
            self.repos.append(repo)
        
        if len(self.repos) == 0:
            print("No repo added. No modules will be available to download.")
        
        root_path = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
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
    
    def get_module(self, module_name: str):
        for mod in self.modules:
            if mod.manifest.name == module_name:
                return mod
        return None
    
    def add_repo(self, repo_url):
        repo_urls_list = [repo.url for repo in self.repos]
        if repo_url in repo_urls_list:
            print(termcolor.colored("Repo already in list", "green"))
            return
        new_repo = ModulesRepo(repo_url)
        is_valid = new_repo.is_valid_repo()
        if not is_valid:
            print(termcolor.colored("This repo is invalid. It might be a network error.", "red"))
            return
        repo_urls_list.append(repo_url)
        self.repos_cache.write_cache("urls.json", repo_urls_list)
        print(termcolor.colored("Added successfully", "green"))
        
    def get_repo(self, url: str):
        for repo in self.repos:
            if repo.url == url:
                return repo
        return None
        
    def remove_repo(self, repo_url: str):
        repo_urls_list = [repo.url for repo in self.repos]
        if repo_url not in repo_urls_list:
            print(termcolor.colored("Repo is not in list", "green"))
            return
        repo = self.get_repo(repo_url)
        if repo is None:
            print(termcolor.colored("An unknown error occurred. Please try again.", "red"))
            return
        repo.remove_cache()
        repo_urls_list.remove(repo_url)
        self.repos_cache.write_cache("urls.json", repo_urls_list)
        print(termcolor.colored("Removed successfully", "green"))
    

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
    def add_repo(self, repo_url: str):
        module_manager.add_repo(repo_url)
        
    @module_manager_initer
    def remove_repo(self, repo_url: str):
        module_manager.remove_repo(repo_url)
        
    @module_manager_initer
    def list_repos(self):
        print("List of repositories of modules:")
        for repo in module_manager.repos:
            print("Repo at {}".format(termcolor.colored(repo.url, "green")))
        if len(module_manager.repos) == 0:
            print("No repo.")
    
    @module_manager_initer
    def list(self):
        if len(module_manager.modules) == 0:
            print("No module installed")
            return
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
    def install(self, module: str, update: bool = False, repo: str = None):
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
            termcolor.colored(version, "cyan")
        ))
        if not update and module_name in module_manager.get_module_names():
            print(termcolor.colored("Module already installed", "green"))
            return
        
        repos_having_it = []
        for r in module_manager.repos:
            if repo:
                if r.url == repo and r.has_module(module_name):
                    repos_having_it.append(r)
                    break
            else:
                if r.has_module(module_name):
                    repos_having_it.append(r)
                
        if len(repos_having_it) > 1:
            print("More than 1 repo has a module named {}:".format(
                termcolor.colored(module_name, "green")                                                    
            ))
            for repo in repos_having_it:
                print(repo.url)
            print("Specify the repo you want to use with the flag --repo")
            print("e.g.: --repo \"{}\"".format(
                repos_having_it[0].url.replace("\"", "\\\"")
            ))
            return
        if len(repos_having_it) == 0:
            print("Could not find any repo with a module named {}".format(
                termcolor.colored(module_name, "green")
            ))
            return
        repo_used: ModulesRepo = repos_having_it[0]
        
        print("Using repo {}".format(
            termcolor.colored(repo_used.url, "green")
        ))
        
        if not repo_used.has_module(module_name):
            print(termcolor.colored("Could not find module {}".format(module_name), "red"))
            return
        
        if version != "latest" and not repo_used.module_has_version(module_name, version):
            print(termcolor.colored("Could not find version {} for module {}".format(version, module_name), "red"))
            return
        versions = repo_used.get_module_versions(module_name)

        if versions is None:
            print("Could not fetch versions for module {}.".format(
                termcolor.colored(module_name, "green")
            ))
            return
        
        if version == "latest":
            latest_version = versions.get("latest", None)
            print("Latest version is version {}".format(
                termcolor.colored(latest_version, "cyan")
            ))
            version = latest_version
             
        latest_version = versions.get("latest", None)
        if update and module_name in module_manager.get_module_names():
            module = module_manager.get_module(module_name)
            if module.manifest.version == latest_version:
                print(termcolor.colored("You already have the last version"))
                return
        
        print("Dowloading module...")
        module = repo_used.get_module(module_name, version)
        if module is None:
            print(termcolor.colored("Could not download module {}".format(module_name), "red"))
            return
        manifest, packaged = module
        if not manifest or not packaged:
            print(termcolor.colored("Unable to download module {}".format(module_name), "red"))
            return
        
        if update and module_name in module_manager.get_module_names():
            print("Uninstalling old module...")
            self.uninstall(module_name)
        print("Installing new module...")
        module_id = module_manager.generate_nonce()
        module = Module(module_id, manifest)
        result = module.install(packaged)
        if result:
            print(termcolor.colored("Module installed succesffuly", "green"))

    @module_manager_initer
    def uninstall(self, module_name: str):
        if not module_name in module_manager.get_module_names():
            print(termcolor.colored("There is no installed module with this name"))
            return
        
        module = module_manager.get_module(module_name)
        if not module:
            print(termcolor.colored("Could not find the module. You might need to delete it manually"))
            return
        shutil.rmtree(
            module.module_dir
        )
        print(termcolor.colored("Module uninstalled", "green"))
        