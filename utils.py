import subprocess
import traceback
import os
from sys import platform
from datetime import datetime


def operating_system():
    try:
        if platform == "linux" or platform == "linux2":
            return "linux"
        elif platform == "darwin":
            return "osx"
        elif platform == "win32":
            return "windows"
    except Exception as err_os:
        raise err_os


def timestamp(format):
    try:
        now = datetime.now()
        now_formated = now.strftime(format)
        return now_formated
    except Exception as err_timestamp:
        raise err_timestamp
