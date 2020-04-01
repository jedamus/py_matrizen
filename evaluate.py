#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Mittwoch, 01. April 2020 14:06 (C) 2020 von Leander Jedamus
# modifiziert Mittwoch, 01. April 2020 14:15 von Leander Jedamus

from __future__ import print_function
import numpy as np

mat = "[[0,1],[1,0]]"

str = "np.array(" + mat + ", dtype=np.int8)"

matrix = eval(str)

print(matrix)

# vim:ai sw=2 sts=4 expandtab

