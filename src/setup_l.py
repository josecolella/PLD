

"""
Script used to create a binary for linux
Usage:
    python3 setup_l.py build
"""

import sys
from cx_Freeze import setup, Executable

setup(
    name = "Treasure Hunters",
    version = "0.1",
    description = "Our Game",
    executables = [Executable("main.py", base = "Console")])
