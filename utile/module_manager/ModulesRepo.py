import requests
from utile.CacheManager import JSONCache
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
            return requests.get(url).json()
        except Exception as e:
            print(termcolor.colored("Unable to fetch versions for module {} ({})".format(module_name, e), "red"))
            return None
    
    def build_modules_cache(self):
        try:
            self.modules = self.requests_session.get(f"{self.url}/modules.json").json()
            return True
        except Exception as e:
            print(termcolor.colored("Unable to fetch repo modules (url: {}, {})".format(self.url, e), "red"))
            return False
        
    def rebuild_cache(self):
        self.build_modules_cache()
        self.get_modules_versions()
        