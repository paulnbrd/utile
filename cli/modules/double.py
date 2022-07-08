# This file is an example module for the docs (https://pol1.gitbook.io/cliutils/modules/how-to-create-a-new-module)
from cli.modules.Module import Module


def execute(number: int):
    return number * 2


class ModuleDouble(Module):
    def get_command_name(self) -> str:
        return "double"
    
    def get_executor(self):
        return execute
    
MODULE = ModuleDouble()
