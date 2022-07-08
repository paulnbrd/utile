class Module:
    def __init__(self) -> None:
        pass
    
    def get_command_name(self) -> str:
        """Returns the command name (package, build, convert...)
        """
        raise NotImplementedError("You must create the method get_command_name to create a module")
    
    def get_executor(self):
        """Returns the function to pass to fire for this command
        """
        raise NotImplementedError("Implement the method get_executor")
    