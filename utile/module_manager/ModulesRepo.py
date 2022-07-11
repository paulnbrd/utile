import os
import shutil
import requests
from utile.CacheManager import JSONCache
from utile.module_manager.Module import Module
from utile.module_manager.manifest import Manifest
import utile.utils
import termcolor

DEFAULT_MODULES_REPO = "https://raw.githubusercontent.com/paulnbrd/utile-modules/master/modules"


class ModulesRepo:
    def __init__(self, url: str):
        self.url = url
        self.requests_session = requests.Session()
        self.cache = JSONCache(utile.utils.Directory.get_cache_path("repos",
                                                                            utile.utils.filename_friendly(self.url)))
        self.modules = self.cache.read_cache("modules")
        if self.modules is None:
            self.build_modules_cache()
        self.versions = {}
        self.get_modules_versions()
        
    def get_modules_versions(self, rebuild_cache: bool = False):
        self.versions = {}
        if self.modules:
            for module in self.modules:
                if rebuild_cache:
                    version = self.fetch_module_versions(module)
                    self.cache.write_cache("versions/{}".format(module), version)
                else:
                    version = self.cache.read_cache("versions/{}".format(module))
                    if not version:
                        version = self.fetch_module_versions(module)
                        self.cache.write_cache("versions/{}".format(module), version)
                self.versions[module] = version
    
    def fetch_module_versions(self, module_name: str):
        url = self.url + "/{}/versions.json".format(module_name)
        try:
            req = requests.get(url)
            req.raise_for_status()
            return req.json()
        except Exception as e:
            print(termcolor.colored("Unable to fetch versions for module {} ({})".format(module_name, e), "red"))
            return None
    
    def build_modules_cache(self):
        try:
            self.modules = self.requests_session.get(f"{self.url}/modules.json").json()
            self.cache.write_cache("modules", self.modules)
            return True
        except Exception as e:
            print(termcolor.colored("Unable to fetch repo modules (url: {}, {})".format(self.url, e), "red"))
            return False
        
    def is_valid_repo(self):
        return self.modules is not None
    
    def remove_cache(self):
        shutil.rmtree(self.cache.base_directory)
    
    def rebuild_cache(self):
        self.remove_cache()
        os.makedirs(self.cache.base_directory, exist_ok=True)
        self.build_modules_cache()
        self.get_modules_versions()
        
    def has_module(self, module_name: str):
        return module_name in self.modules
    
    def get_module_versions(self, module_name: str):
        if module_name not in self.modules:
            return None
        versions = self.cache.read_cache("versions/{}".format(module_name))
        if versions is None:
            versions = self.fetch_module_versions(module_name)
            if versions is not None:
                self.cache.write_cache("versions/{}".format(module_name), versions)
        return versions
    
    def module_has_version(self, module_name: str, version: str):
        versions = self.get_module_versions(module_name)
        if versions is None:
            return False
        for vers in versions.get("list", []):
            if vers == version:
                return True
        return False
    
    def get_module_manifest(self, module_name: str, version: str):
        url = f"{self.url}/{module_name}/{version}/manifest.json"
        cached = self.cache.read_cache(f"module/{module_name}/manifest")
        if cached:
            return Manifest(cached)
        try:
            req = requests.get(url)
            req.raise_for_status()
            data = req.json()
            self.cache.write_cache(f"module/{module_name}/manifest", data)
            return Manifest(data)
        except:
            return None
        
    def get_module_packaged(self, module_name: str, version: str):
        url = f"{self.url}/{module_name}/{version}/packaged.module"
        cached = self.cache.read_cache(f"module/{module_name}/packaged")
        if cached:
            return cached
        try:
            req = requests.get(url)
            req.raise_for_status()
            data = req.text
            self.cache.write_cache(f"module/{module_name}/packaged", data)
            return data
        except Exception as e:
            return None
    
    def get_module(self, module_name: str, version: str):
        if not self.module_has_version(module_name, version):
            return None
        manifest = self.get_module_manifest(module_name, version)
        packaged = self.get_module_packaged(module_name, version)
        return manifest, packaged
        