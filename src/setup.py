

"""
Script used to create a binary for mac
Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']  # The name of the application
DATA_FILES = [('', ['img']), ('', ['audio'])]
OPTIONS = {'iconfile': 'icon.icns', }  # 'argv_emulation': False/True

setup(

    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],

)
