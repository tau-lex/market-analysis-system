# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Market Analysis System                                                    #
#   https://www.mql5.com/ru/users/terentyev23                                 #
#                                                                             #
#   M A R K E T   A N A L Y S I S   S C R I P T   W I T H   K E R A S         #
#                                                                             #
#   Aleksey Terentyev                                                         #
#   terentew.aleksey@ya.ru                                                    #
#                                                                             #
###############################################################################
"""
The module contains functions for the MAS project.
"""

import sys


def get_parameters():
    """Returns a list of parameters."""

    idx = 0
    result = []

    for item in sys.argv:
        if idx > 0:
            result.append(item)
        idx += 1

    return result
