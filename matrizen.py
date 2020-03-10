#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Dienstag, 10. März 2020 10:55 (C) 2020 von Leander Jedamus
# modifiziert Dienstag, 10. März 2020 11:10 von Leander Jedamus

from __future__ import print_function

n = 3
for i in range(2**n):
  print(i+1)
  for j in range(n):
    if (i & 2**(n-j-1) != 0):
      print("1",end="")
    else:
      print("0",end="")
  print()

# vim:ai sw=2 sts=4 expandtab

