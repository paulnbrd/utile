import os
import sys
from utile.module_manager.Module import Module


class ModulesLoader:
    def __init__(self) -> None:
        self.modules_dir = os.path.realpath(
            os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), "modules")
        )
        
        self.module_ids = [i for i in os.listdir(self.modules_dir) if os.path.isdir(
            os.path.join(self.modules_dir, i)
        )]
        self.modules: list[Module] = [
            Module(id) for id in self.module_ids
        ]
