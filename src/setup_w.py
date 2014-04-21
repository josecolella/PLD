

"""
Script used to create a binary for windows
Usage:
    python.exe setup_w.py build
"""

import sys
from cx_Freeze import setup, Executable

setup(
    name = "Treasure Hunters",
    version = "0.1",
    description = "Our Game",
    executables = [Executable("main.py", base = "Win32GUI")])
