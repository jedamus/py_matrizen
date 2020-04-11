#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Dienstag, 31. März 2020 20:31 (C) 2020 von Leander Jedamus
# modifiziert Samstag, 11. April 2020 15:16 von Leander Jedamus
# modifiziert Dienstag, 31. März 2020 20:46 von Leander Jedamus

from __future__ import print_function
import logging
import matrizen

logger = logging.getLogger(__name__)

def matrix_create(n=2,filename="matrix_test.dat"):
  try:
    datei = open(filename,"w")
    datei.write(_("# file is {filename:s}\n").format(filename=filename))

    datei.write("\n")
    datei.write("n = {n:d}\n".format(n=n))

    datei.write("\n")
    datei.write("# bits:\n")
    bits = matrizen.get_bits(n)

    power = 2**n

    for i in range(power):
      datei.write("{input:s} > {output:s}\n".format(input=bits[i], output=bits[0]))
    datei.close()
  except IOError as e:
    logger.fatal(e)
    exit(-1)

# vim:ai sw=2 sts=4 expandtab

