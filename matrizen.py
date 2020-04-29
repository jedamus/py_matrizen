#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 11. April 2020 15:17 (C) 2020 von Leander Jedamus
# modifiziert Mittwoch, 29. April 2020 12:51 von Leander Jedamus
# modifiziert Samstag, 11. April 2020 15:18 von Leander Jedamus

from __future__ import print_function
import os
import inspect
import logging

logger = logging.getLogger(__name__)

scriptpath = os.path.realpath(os.path.abspath(os.path.split( \
               inspect.getfile(inspect.currentframe()))[0]))

def get_bits(n):
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

# vim:ai sw=2 sts=4 expandtab

