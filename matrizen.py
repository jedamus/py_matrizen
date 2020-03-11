#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Dienstag, 10. März 2020 10:55 (C) 2020 von Leander Jedamus
# modifiziert Mittwoch, 11. März 2020 10:59 von Leander Jedamus
# modifiziert Dienstag, 10. März 2020 11:32 von Leander Jedamus

from __future__ import print_function

import sys
if int(sys.version_info.major) < 3:
  my_input = raw_input
else:
  my_input = input

import os
import sys
import logging

log_path_and_filename = os.path.join("/tmp","matrizen.log")
file_handler = logging.FileHandler(log_path_and_filename)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s",
                              "%d.%m.%Y %H:%M:%S")
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
log = logging.getLogger()
log.addHandler(file_handler)
log.addHandler(stdout_handler)
# log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)

def mat_mul(s_vector,z_vector,n):
  power = 2**n
  mat = [];
  for i in range(power):
    mat.append([])

  for i in range(power):
    for j in range(power):
      mat[i-1].append(0)

  for i in range(power):
    for j in range(power):
      mat[i-1][j-1]= s_vector[i-1]*z_vector[j-1]
  
  return(mat)

inp = my_input('n = ')
if inp.isdigit():
  n = int(inp)
  power = 2**n
  bits = [];
  vec_s = [];
  vector = [];
  mat = [];
  for i in range(power):
    bits.append("")
    vec_s.append("")
    vector.append([]);

  for i in range(power):
    for j in range(power):
      vector[j-1].append(0)

  log.debug("vector = {vector:s}".format(vector=str(vector)))

  for i in range(power):
    log.debug("i = {i:s}".format(i=str(i+1)))
    for j in range(n):
      if (i & 2**(n-j-1) != 0):
        bits[i-1] += "1"
      else:
        bits[i-1] += "0"
    log.debug("bits[{i:d}] = {bits:s}".format(i=i,bits=bits[i-1]))
    for j in range(power):
      if (j == i):
        vec_s[i-1] += "1"
        vector[i-1][j-1] = 1
      else:
        vec_s[i-1] += "0"
    log.debug("vec_s[{i:d}] = {vec_s:s}".format(i=i,vec_s=vec_s[i-1]))
  log.debug("vector = {vector:s}".format(vector=str(vector)))

  # bra und ket einlesen
  mat.append(mat_mul(vector[3],vector[2],n))
  log.info("mat[0] = {mat:s}".format(mat=str(mat[0])))

# vim:ai sw=2 sts=4 expandtab

