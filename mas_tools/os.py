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

def get_api_pair(filename):
    """
    Return api key-secret pair from file.
    """

    key, secret = '', ''

    ## Read file in to lines list
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        if line.find('KEY', 0, 7) > 0:
            key = line.split('=')[1]
        if line.find('SECRET', 0, 10) > 0:
            secret = line.split('=')[1]

    return key, secret         