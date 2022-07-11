import os
import sys
from utile.module_manager.Module import Module


class ModulesLoader:
    def __init__(self) -> None:
        root_path = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
        self.modules_dir = os.path.realpath(
            os.path.join(root_path, "modules")
        )
        os.makedirs(self.modules_dir, exist_ok=True)
        
        self.module_ids = [i for i in os.listdir(self.modules_dir) if os.path.isdir(
            os.path.join(self.modules_dir, i)
        ) and i.startswith("m")]
        self.modules: list[Module] = [
            Module(id) for id in self.module_ids
        ]
