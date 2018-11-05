import inspect
import os
import sys


def get_home():
    """
    Returns the path to the user directory.
    """

    return os.path.expanduser("~")


def get_parameters():
    """
    Returns a list of parameters (without filename).
    """

    return sys.argv[1:]


def get_script_dir(follow_symlinks=True):
    """
    Return script file directory.
    from: https://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory/22881871#22881871

    PS. Return this script path. =)
    Use inline.
    """

    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)

    return os.path.dirname(path)
