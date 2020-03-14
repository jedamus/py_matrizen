#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 07:37 (C) 2020 von Leander Jedamus
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
  datei = open(filename,"r")
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

    if logger.isEnabledFor(logging.DEBUG):
      logger.debug("line = " + line)

    if not has_n:
      # n auslesen
      if (re.match(reg_n,line)):
        if logger.isEnabledFor(logging.DEBUG):
          logger.debug(_("found n"))
        n = re.sub(reg_n,"\g<1>",line)
        if n.isdigit():
          n = int(n)
          has_n = True
          logger.debug("n = " + str(n))

          (bits,vector) = matrizen.bits_and_vector(n)
          logger.debug("bits = " + str(bits))
          logger.debug("vector = " + str(vector))

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
        if logger.isEnabledFor(logging.DEBUG):
          logger.debug(_("found bits"))
        line = re.sub(reg_bits,"\g<1> \g<2>",line)
        lbits = re.sub(reg_lbits,"\g<1>",line)
        rbits = re.sub(reg_rbits,"\g<1>",line)
        if logger.isEnabledFor(logging.DEBUG):
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
          if logger.isEnabledFor(logging.DEBUG):
            logger.debug(_("index of rbits = {i:d}").format(i=i))

      if((s_index == -1) or (z_index == -1)):
        if logger.isEnabledFor(logging.ERROR):
          logger.error(_("bits not found in line {line_no:d}").format(line_no=line_no))
      else:
        if(has_bits[s_index]):
          if logger.isEnabledFor(logging.ERROR):
            logger.error(_("bits double in line {line_no:d}").format(line_no=line_no))
        else:
          has_bits[s_index] = True

        bits_count += 1
        s_vector = vector[s_index]
        z_vector = vector[z_index]
        mat = matrizen.mat_mul(s_vector,z_vector,n)
        if logger.isEnabledFor(logging.DEBUG):
          logger.debug("mat = {mat:s}".format(mat=str(mat)))

        for i in range(power):
          for j in range(power):
            matrix[i][j] += mat[i][j]

  datei.close()

  if(bits_count > power):
    if logger.isEnabledFor(logging.ERROR):
      logger.error(_("too many bits in file"))
    exit(-1)
  elif(bits_count < power):         
    if logger.isEnabledFor(logging.ERROR):
      logger.error(_("not enough bits in file"))
    exit(-1)

  logger.info("matrix = {matrix:s}".format(matrix=str(matrix)))
  return(matrix)

# vim:ai sw=2 sts=4 expandtab

