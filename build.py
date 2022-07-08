import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"excludes": ["tkinter"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None

setup(
    name="utile",
    version="0.1",
    description="Utile CLI",
    options={"build_exe": build_exe_options},
    executables=[Executable("utile.py", base=base)],
)
