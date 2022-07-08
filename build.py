import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "excludes": ["tkinter"],
    "includes": [],
    "packages": ["utile"]
}
modules = os.listdir("utile/modules")
modules = [module.removesuffix(".py") for module in modules
           if os.path.isfile("utile/modules/{}".format(module)) and module != "__init__.py"]
if "Module" in modules:
    modules.remove("Module")
build_exe_options["includes"] = ["utile.modules.{}".format(module) for module in modules]
print(build_exe_options["includes"])

# base="Win32GUI" should be used only for Windows GUI app
base = None

setup(
    name="utile",
    version="0.1",
    description="Utile CLI",
    options={"build_exe": build_exe_options},
    executables=[Executable("utile.py", base=base)],
)
