---
description: This page describes how you can create your own modules !
---

# How to create a new module

To create a new module, you first need to create a new Python file, under cli/modules. For example, I want to create a module that double the number that we give to it. I create a file named double.py (the name doesn't matter), and begin to edit it.

We then need to create a sort of "module manifest" by creating a class that inherits the Module class (cli.modules.Module.Module). For the example module, I can do that like so:

```python
from cli.modules.Module import Module


class ModuleDouble(Module):
    pass

```

You need to define the command name, which will be the keywork just after the CLIUtils command:

`<CLIUtils command> <command name>`

To do that, modify your module class to implement the function to get the command name:

```python
class ModuleDouble(Module):
    def get_command_name(self) -> str:
        return "double"
```

This module has the command name `double` and can now be invoked with it

We now need to define a function to do the actual work of the module. We will call it here execute, but you can call it however you want.

```python
def execute(number: int):
    return number * 2
```

The returned object will be the new executor. See Google Fire docs to understand how it is handled, but basically, all the methods of the object now becomes subcommands. In this case, we don't want the user to be able to do stuff on the result number, so we will just print it.

```python
def execute(number: int):
    print(number * 2)
```

For example, you can make another execute function to be able to have more subcommands. It is basically the executor of your executor.

Now, we just need to define the executor for our module

```python
class ModuleDouble(Module):
    def get_command_name(self) -> str:
        return "double"
    
    def get_executor(self):
        return execute
```

And at the end of the file, make the module public by creating an instance of the ModuleDouble class and assign the MODULE variable to it:

```python
MODULE = ModuleDouble()
```

Like so, the module can be imported by the CLI, and is now ready to be used !

We can use our newly created module like so:

```
<CLIUtils command> double <number>

// For example
<CLIUtils command> double 2
// Prints 4
```

This example module is available in the repo modules folder (is available to anyone who has the program) [here](https://github.com/paulnbrd/CLI/cli/modules/double.py)
