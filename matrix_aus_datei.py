#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 07:37 (C) 2020 von Leander Jedamus
# modifiziert Montag, 16. März 2020 13:18 von Leander Jedamus
# modifiziert Sonntag, 15. März 2020 14:21 von Leander Jedamus
# modified Sunday, 15. March 2020 06:55 by Leander Jedamus
# modifiziert Sonntag, 15. März 2020 06:53 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 13:59 von Leander Jedamus

from __future__ import print_function
import re
import os
import sys
import logging
import matrizen

logger = logging.getLogger(__name__)

import os
import sys
import gettext

scriptpath = os.path.abspath(os.path.dirname(sys.argv[0]))
try:
  trans = gettext.translation("matrizen",os.path.join(scriptpath, "translate"))
  trans.install(unicode=True)
except IOError:
  logger.error("Fehler in gettext")
  def _(s):
    return s

def matrix_aus_datei(filename="matrix_cnot.dat"):
  try:
    datei = open(filename,"r")
  except IOError as e:
    logger.fatal(e)
    exit(-1)

  debug_enabled = logger.isEnabledFor(logging.DEBUG)
  error_enabled = logger.isEnabledFor(logging.ERROR)

  reg_comment = re.compile(r"^#.*")
  reg_empty = re.compile(r"^$")
  reg_n = re.compile(r"n = (\d+)")
  reg_bits = re.compile(r"([01]+) > ([01]+)")
  reg_lbits = re.compile(r"([01]+) [01]+")
  reg_rbits = re.compile(r"[01]+ ([01]+)")

  has_n = False
  has_bits = []
  line_no = 0
  bits_count = 0
  matrix = []
  for line in datei:
    line_no += 1
    # Kommentare ausfiltern
    if (re.match(reg_comment,line)):
      continue

    line = line.strip()
    # leere Zeilen ausfiltern
    if (re.match(reg_empty,line)):
      continue

    if debug_enabled:
      logger.debug("line = " + line)

    if not has_n:
      # n auslesen
      if (re.match(reg_n,line)):
        if debug_enabled:
          logger.debug(_("found n"))
        n = re.sub(reg_n,"\g<1>",line)
        if n.isdigit():
          n = int(n)
          has_n = True
          if debug_enabled:
            logger.debug("n = {n:d}".format(n=n))

          (bits,vector) = matrizen.bits_and_vector(n)
          if debug_enabled:
            logger.debug("bits = {bits:s}".format(bits=bits))
            logger.debug("vector = {vector:s}".format(vector=vector))

          power = 2**n
          for i in range(power):
            has_bits.append(False)
            matrix.append([])

          for i in range(power):
            for j in range(power):
              matrix[j].append(0)

        else:
          logger.fatal(_("n is not a decimal"))
    else:
      if (re.match(reg_bits,line)):
        if debug_enabled:
          logger.debug(_("found bits"))
        line = re.sub(reg_bits,"\g<1> \g<2>",line)
        lbits = re.sub(reg_lbits,"\g<1>",line)
        rbits = re.sub(reg_rbits,"\g<1>",line)
        if debug_enabled:
          logger.debug("lbits = " + lbits)
          logger.debug("rbits = " + rbits)

      # lbits und rbits suchen und index merken
      s_index = -1
      z_index = -1
      for i in range(power):
        if lbits == bits[i]:
          s_index = i
          if logger.isEnabledFor(logging.DEBUG):
            logger.debug(_("index of lbits = {i:d}").format(i=i))
        if rbits == bits[i]:
          z_index = i
          if debug_enabled:
            logger.debug(_("index of rbits = {i:d}").format(i=i))

      if((s_index == -1) or (z_index == -1)):
        if error_enabled:
          logger.error(_("bits not found in line {line_no:d}").format(line_no=line_no))
      else:
        if(has_bits[s_index]):
          if error_enabled:
            logger.error(_("bits double in line {line_no:d}").format(line_no=line_no))
        else:
          has_bits[s_index] = True

        bits_count += 1
        s_vector = vector[s_index]
        z_vector = vector[z_index]
        mat = matrizen.mat_mul(s_vector,z_vector,n)
        if debug_enabled:
          logger.debug("mat = {mat:s}".format(mat=mat))

        for i in range(power):
          for j in range(power):
            matrix[i][j] += mat[i][j]

  if not has_n:
    logger.fatal(_("No n defined!"))
    exit(-1)
  datei.close()

  if(bits_count > power):
    if logger.isEnabledFor(logging.ERROR):
      logger.fatal(_("too many bits in file"))
    exit(-1)
  elif(bits_count < power):         
    if logger.isEnabledFor(logging.ERROR):
      logger.fatal(_("not enough bits in file"))
    exit(-1)

  logger.debug("matrix = {matrix:s}".format(matrix=matrix))
  return(matrix)

# vim:ai sw=2 sts=4 expandtab

