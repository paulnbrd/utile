import os
import json


class CacheManager:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory
        self.cache_cache = {}
        os.makedirs(self.base_directory, exist_ok=True)

    def get_path(self, file: str):
        path = os.path.realpath(os.path.join(self.base_directory, file))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path
    
    def write_cache(self, file: str, data, *, mode: str = "wb"):
        path = self.get_path(file)
        with open(path, mode) as f:
            f.write(data)
            
    def read_cache(self, file: str, *, file_mode: str= "rb", allow_from_cache: bool = True):
        path = self.get_path(file)
        if allow_from_cache and path in self.cache_cache.keys():
            return self.cache_cache.get(path)
        if not os.path.isfile(path):
            return None
        with open(path, file_mode) as f:
            content = f.read()    
        self.cache_cache[path] = content
        return content
    
    def has_cache(self, file: str):
        content = self.read_cache(file)
        return content is not None


class JSONCache(CacheManager):
    def read_cache(self, file: str, *, allow_from_cache: bool = True):
        data = super().read_cache(file, allow_from_cache=allow_from_cache)
        try:
            decoded = json.loads(data)
            return decoded
        except:
            return None
    
    def write_cache(self, file: str, data: dict):
        encoded = json.dumps(data)
        super().write_cache(file, encoded, mode="w")
