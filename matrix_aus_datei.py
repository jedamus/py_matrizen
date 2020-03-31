#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 07:37 (C) 2020 von Leander Jedamus
# modifiziert Dienstag, 31. März 2020 22:51 von Leander Jedamus
# modifiziert Freitag, 20. März 2020 09:41 von Leander Jedamus
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
import numpy as np
import matrizen

logger = logging.getLogger(__name__)

import os
import sys
import gettext

scriptpath = os.path.abspath(os.path.dirname(sys.argv[0]))
try:
  trans = gettext.translation("matrizen",os.path.join(scriptpath, "translate"))
# trans.install(unicode=True)
  trans.install()
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

          power = 2**n
          matrix = np.zeros( (power,power), dtype=np.int8 )
          for i in range(power):
            has_bits.append(False)

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
        if (len(lbits) != n) | (len(rbits) != n):
          logger.fatal(_("bits not of length {power:d}").format(power=power))
          exit(-1)
        else:  
          s_index = int(lbits,2)
          z_index = int(rbits,2)
          if debug_enabled:
            logger.debug("s_index = {s_index:d}".format(s_index=s_index))
            logger.debug("z_index = {z_index:d}".format(z_index=z_index))

          if(has_bits[s_index]):
            if error_enabled:
              logger.error(_("bits double in line {line_no:d}").format(line_no=line_no))
          else:
            has_bits[s_index] = True

            bits_count += 1
            s_vector = np.zeros( (power,1), dtype=np.int8 )
            s_vector[s_index][0] = 1
            z_vector = np.zeros( (1,power), dtype=np.int8 )
            z_vector[0][z_index] = 1

            matrix += s_vector*z_vector
      else:
        logger.fatal(_("Line doesn't match"))
        exit(-1)

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

  logger.debug("matrix = {matrix:s}".format(matrix=str(matrix)))
  return(matrix)

# vim:ai sw=2 sts=4 expandtab

