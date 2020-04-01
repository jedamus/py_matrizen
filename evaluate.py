#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Mittwoch, 01. April 2020 14:06 (C) 2020 von Leander Jedamus
# modifiziert Mittwoch, 01. April 2020 15:40 von Leander Jedamus

from __future__ import print_function
import logging
import numpy as np

logger = logging.getLogger(__name__)

mat = "[[0,1],[1,0]]"

str = "np.array(" + mat + ", dtype=np.int8)"
matrix = eval(str)
print("matrix = {matrix:s}".format(matrix=np.array_str(matrix)))
print("matrix.shape = ", matrix.shape)

try:
  datei = open("matrix_xor.mat","r")
  mat = ""
  for line in datei:
    mat += line.strip()
  datei.close()
  str = "np.array(" + mat + ", dtype=np.int8)"
  matrix = eval(str)
  print("matrix = {matrix:s}".format(matrix=np.array_str(matrix)))
except IOError as e:
  logger.fatal(e)
  exit(-1)

# vim:ai sw=2 sts=4 expandtab

