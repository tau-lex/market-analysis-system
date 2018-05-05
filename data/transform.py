#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
from datetime import datetime


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


directory = get_script_dir()

files = os.listdir(directory + '/exported')

files_tf_one = list(filter(lambda x: x.endswith('240.csv'), files))

print(files_tf_one)


# for filename in files_tf_one:
filename = files_tf_one[0]
table = 

print(table)
#datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
# new_table = np.column_stack((np.array(list(map(lambda x: datetime.strptime(x, '%Y.%m.%d'), table[:, 0].astype(np.str)))) + 
#                              np.array(list(map(lambda x: datetime.strptime(x, '%H:%M'), table[:, 1].astype(np.str)))),
#                              table[:, 2:]
#                             ))

np.savetxt(directory + '/transformed/' + filename, table, delimiter=';')

