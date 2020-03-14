#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 07:37 (C) 2020 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 07:55 von Leander Jedamus

from __future__ import print_function
import re

datei = open("matrix_xor.dat","r")
reg = re.compile(r"n = (\d+)")
for line in datei:
  line = line.strip()
  if (re.match(reg,line)):
    print("n gefunden")
  print(line)
datei.close()

# vim:ai sw=2 sts=4 expandtab

