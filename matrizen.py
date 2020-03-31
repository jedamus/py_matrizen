#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 08:23 (C) 2020 von Leander Jedamus
# modifiziert Dienstag, 31. März 2020 19:09 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 08:44 von Leander Jedamus

from __future__ import print_function
import logging
import numpy as np

logger = logging.getLogger(__name__)

def bits_and_vector(n):
  power = 2**n
  bits = []
  for i in range(power):
    bits.append("")

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
  return(bits)

def mat_init(n):
  power = 2**n
  return(np.zeros( (power, power), dtype=np.int8 ))

def mat_mul(s_vector,z_vector,n):

  return(s_vector * z_vector)

# vim:ai sw=2 sts=4 expandtab

