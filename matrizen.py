#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 08:23 (C) 2020 von Leander Jedamus
# modifiziert Dienstag, 31. März 2020 18:41 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 08:44 von Leander Jedamus

from __future__ import print_function
import logging
import numpy as np

logger = logging.getLogger(__name__)

def bits_and_vector(n):
  power = 2**n
  bits = []
  ## vector = []
  for i in range(power):
    bits.append("")
    ## vector.append( np.zeros( (1,power), dtype=np.int8 ))

  ## if logger.isEnabledFor(logging.DEBUG):
    ## logger.debug("vector = {vector:s}".format(vector=str(vector)))

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
    ## for j in range(power):
      ## if (j == i):
        ## vector[i][0][j] = 1
  ## if logger.isEnabledFor(logging.DEBUG):
    ## logger.debug("vector = {vector:s}".format(vector=str(vector)))
  # ret = (bits,vector)
  # return(ret)
  return(bits)

def mat_init(n):
  power = 2**n
  return(np.zeros( (power, power), dtype=np.int8 ))

def mat_mul(s_vector,z_vector,n):

  return(s_vector * z_vector)

# vim:ai sw=2 sts=4 expandtab

