#!/usr/bin/env python
import os
import numpy as np
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


directory = get_script_dir()

files = os.listdir(directory + '/transformed')

# '1', '5' and not x[6:8].isdigit(), '15', '30', '60',
# '240', '1440', '10080', '43200'
minor, major = '15', '60'
files_minor = list(filter(lambda x: x.endswith(minor+'.csv'), files))
files_major = list(filter(lambda x: x.endswith(major+'.csv'), files))

# print(files_origin)
# print(files_older)

for idx in range(len(files_minor)):
    f1 = files_minor[idx]
    f2 = files_major[idx]
    newf = f1[:f1.find('.csv')] + '-' + major + '.csv'

    table1 = pd.read_csv(directory + '/transformed/' + f1, sep=';', header=None, parse_dates=True)
    table2 = pd.read_csv(directory + '/transformed/' + f2, sep=';', header=None, parse_dates=True)

    # table1[0] = pd.to_datetime(table1[0])
    # table2[0] = pd.to_datetime(table2[0])

    new_table = np.zeros(0, dtype={'names':('time', 'o1', 'h1', 'l1', 'c1', 'v1', 'o2', 'h2', 'l2', 'c2', 'v2'),
                                'formats':('S16', 'f8', 'f8', 'f8', 'f8', 'i4', 'f8', 'f8', 'f8', 'f8', 'i4')})

    idx2 = 0
    for idx1 in range(len(table1)):
        try:
            if idx2 != len(table2)-1:
                if table1.iloc[idx1, 0] >= table2.iloc[idx2+1, 0]:
                    idx2 += 1
        except:
            print(f1, idx1, f2, idx2)
        if table1.iloc[idx1, 0] < table2.iloc[idx2, 0]:
            continue
        # if table1.iloc[idx1, 0] >= table2.iloc[idx2, 0] and table1.iloc[idx1, 0] < table2.iloc[idx2+1, 0]:
        new_row = np.append(np.array(table1.iloc[idx1].values), table2.iloc[idx2, 1:].values)
        new_table = np.append(new_table, new_row)

    new_table = new_table.reshape((int(new_table.shape[0]/11), 11))
    new_table = pd.DataFrame(new_table)
    # print(new_table)

    new_table.to_csv(directory + '/fractal dataset/' + newf, sep=';',
                     header=False, index=False,
                     date_format="%Y.%m.%d %H:%M")
