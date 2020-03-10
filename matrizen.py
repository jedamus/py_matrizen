#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Dienstag, 10. März 2020 10:55 (C) 2020 von Leander Jedamus
# modifiziert Dienstag, 10. März 2020 11:32 von Leander Jedamus

from __future__ import print_function

n = 3
bits = [];
vector = [];
for i in range(2**n):
  bits.append("")
  vector.append("")
for i in range(2**n):
  print(i+1)
  for j in range(n):
    if (i & 2**(n-j-1) != 0):
      #print("1",end="")
      bits[i-1] += "1"
    else:
      #print("0",end="")
      bits[i-1] += "0"
  print(bits[i-1])
  for j in range(2**n):
    if (j == i):
      #print("1",end="")
      vector[i-1] += "1"
    else:
      #print("0",end="")
      vector[i-1] += "0"
  print(vector[i-1])


# vim:ai sw=2 sts=4 expandtab

