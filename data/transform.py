#!/usr/bin/env python
import os
import pandas as pd


def get_script_dir(follow_symlinks=True):
    """https://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory/22881871#22881871"""
    import inspect
    import os
    import sys
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

## Files list
directory = get_script_dir()
files = list(filter(lambda x: x.endswith('.csv'), os.listdir(directory+'/exported')))

for filename in files:
    ## Read
    table = pd.read_csv(directory + '/exported/' + filename, sep=',', header=None)
    ## Format time
    table[1] = pd.to_datetime(table[0] + ' ' + table[1])
    table.drop([0], axis='columns')
    ## Save
    table.to_csv(directory + '/transformed/' + filename, sep=';',
                    header=False, index=False,
                    date_format="%Y.%m.%d %H:%M")
