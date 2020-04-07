#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Mittwoch, 01. April 2020 14:06 (C) 2020 von Leander Jedamus
# modifiziert Mittwoch, 01. April 2020 16:31 von Leander Jedamus

from __future__ import print_function
import logging
import numpy as np

logger = logging.getLogger(__name__)

matname = "matrix_test.mat"

mat = "[[0,1],[1,0]]"

str = "np.array(" + mat + ", dtype=np.int8)"
matrix = eval(str)
print("matrix = {matrix:s}".format(matrix=np.array_str(matrix)))
print("matrix.shape = ", matrix.shape)

try:
  datei = open(matname,"r")
  print("Reading  \"{matname:s}\"".format(matname=matname))
  str = "np.array("
  count = 0
  for line in datei:
    str += line.strip()
    count += 1
    print(count,"...", end="")
  datei.close()
  str += ", dtype=np.int8)"
  print("\n\nEval ...", end="")
  matrix = eval(str)
  print("done.")
  print("matrix = {matrix:s}".format(matrix=np.array_str(matrix)))
except IOError as e:
  logger.fatal(e)
  exit(-1)

# vim:ai sw=2 sts=4 expandtab

