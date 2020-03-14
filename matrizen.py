#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 08:23 (C) 2020 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 08:44 von Leander Jedamus

from __future__ import print_function
import logging

logger = logging.getLogger(__name__)

def bits_and_vector(n):
  power = 2**n
  bits = []
  vec_s = []
  vector = []
  matrix = []
  for i in range(power):
    bits.append("")
    vec_s.append("")
    vector.append([])
    matrix.append([])

  for i in range(power):
    for j in range(power):
      vector[j].append(0)
      matrix[j].append(0)

  if logger.isEnabledFor(logging.DEBUG):
    logger.debug("vector = {vector:s}".format(vector=str(vector)))

  for i in range(power):
    if logger.isEnabledFor(logging.DEBUG):
      logger.debug("i = {i:s}".format(i=str(i+1)))
    for j in range(n):
      if (i & 2**(n-j-1) != 0):
        bits[i] += "1"
      else:
        bits[i] += "0"
    if logger.isEnabledFor(logging.DEBUG):
      logger.debug("bits[{i:d}] = {bits:s}".format(i=i,bits=bits[i]))
    for j in range(power):
      if (j == i):
        vec_s[i] += "1"
        vector[i][j] = 1
      else:
        vec_s[i] += "0"
    if logger.isEnabledFor(logging.DEBUG):
      logger.debug("vec_s[{i:d}] = {vec_s:s}".format(i=i,vec_s=vec_s[i]))
  if logger.isEnabledFor(logging.DEBUG):
    logger.debug("vector = {vector:s}".format(vector=str(vector)))
  ret = (bits,vector)
  return(ret)

def mat_init(n):
  power = 2**n
  mat = [];
  for i in range(power):
    mat.append([])

  for i in range(power):
    for j in range(power):
      mat[i-1].append(0)

  return(mat)

def mat_mul(s_vector,z_vector,n):

  mat = mat_init(n)
  power = 2**n

  for i in range(power):
    for j in range(power):
      mat[i-1][j-1]= s_vector[i-1]*z_vector[j-1]

  return(mat)

# vim:ai sw=2 sts=4 expandtab

