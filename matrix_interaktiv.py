#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Dienstag, 10. März 2020 10:55 (C) 2020 von Leander Jedamus
# modified Sunday, 15. March 2020 07:17 by Leander Jedamus
# modifiziert Samstag, 14. März 2020 14:15 von Leander Jedamus
# modified Saturday, 14. March 2020 14:13 by Leander Jedamus
# modifiziert Samstag, 14. März 2020 13:25 von Leander Jedamus
# modifiziert Mittwoch, 11. März 2020 17:35 von Leander Jedamus
# modifiziert Dienstag, 10. März 2020 11:32 von Leander Jedamus

from __future__ import print_function
import logging
import matrizen
import sys
import os
import gettext

if int(sys.version_info.major) < 3:
  my_input = raw_input
else:
  my_input = input

logger = logging.getLogger(__name__)

scriptpath = os.path.abspath(os.path.dirname(sys.argv[0]))
try:
  trans = gettext.translation("matrizen",os.path.join(scriptpath, "translate"))
  trans.install(unicode=True)
except IOError:
  logger.error("Fehler in gettext")
  def _(s):
    return s

"""
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
"""

def matrix_interaktiv():
  while(True):
    inp = my_input('n = ')
    if not inp.isdigit():
      print(_("Wrong input!"))
    else:
      n = int(inp)
      if (n>1):
        break
      else:
        print(_("Wrong input!"))

  (bits, vector) = matrizen.bits_and_vector(n)
  power = 2**n
  matrix = []
  for i in range(power):
    matrix.append([])

  for i in range(power):
    for j in range(power):
      matrix[j].append(0)

  # bra und ket einlesen
  bra = []
  bra_ind = []
  for i in range(power):
    bra.append("{i:d}. {bra:s}".format(i=i+1,bra=bits[i]))
    bra_ind.append(i)
  if logger.isEnabledFor(logging.DEBUG):
    logger.debug("bra_ind = {bra_ind:s}".format(bra_ind=str(bra_ind)))
  bras = power
  while(bras > 0):
    for i in range(power):
      if bra[i] != "":
        print(bra[i])

    j = my_input(_('Wich bra (input vector):'))
    if not j.isdigit():
      print(_("Wrong input!"))
    else: 
      j = int(j)
      if (j<=0) or (j>power):
        print(_("Wrong input!"))
      else:
        if bra[j-1] == "":
          print(_("Wrong input!"))
        else:
          bra[j-1] = ""
          if logger.isEnabledFor(logging.DEBUG):
            logger.debug("bits = {bits:s}".format(bits=str(bits)))
            logger.debug("bits[{index:d}] = {bits:s}".format(index=bra_ind[j-1],bits=bits[bra_ind[j-1]]))
          bras -= 1
          s_vector = vector[bra_ind[j-1]]
          if logger.isEnabledFor(logging.DEBUG):
            logger.debug("{s_vector:s}".format(s_vector=s_vector))

          ket = []
          ket_ind = []
          for i in range(power):
            ket.append("{i:d}. {ket:s}".format(i=i+1,ket=bits[i]))
            ket_ind.append(i)
          if logger.isEnabledFor(logging.DEBUG):
            logger.debug("ket_ind = {ket_ind:s}".format(ket_ind=str(ket_ind)))

          while(True):
            for i in range(power):
              if ket[i] != "":
                print(ket[i])

            k = my_input(_('Wich Ket (output vector):'))
            if not k.isdigit():
              print(_("Wrong input!"))
            else:
              k = int(k)
              if (k<=0) or (k>power):
                print(_("Wrong input!"))
              else:
                ket[k-1] = ""
                z_vector = vector[ket_ind[k-1]]
                mat = matrizen.mat_mul(s_vector,z_vector,n)
                if logger.isEnabledFor(logging.DEBUG):
                  logger.debug("bits = {bits:s}".format(bits=str(bits)))
                  logger.debug("bits[{index:d}] = {bits:s}".format(index=ket_ind[k-1],bits=bits[ket_ind[k-1]]))
                  logger.debug("{z_vector:s}".format(z_vector=z_vector))
                  logger.debug("mat = {mat:s}".format(mat=str(mat)))
                break

          for i in range(power):
            for j in range(power):
              matrix[i][j] += mat[i][j]
              
  logger.info("matrix = {matrix:s}".format(matrix=str(matrix)))
  return(matrix)

# vim:ai sw=2 sts=4 expandtab

