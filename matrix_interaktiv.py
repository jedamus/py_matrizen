#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Dienstag, 10. März 2020 10:55 (C) 2020 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 13:25 von Leander Jedamus
# modifiziert Mittwoch, 11. März 2020 17:35 von Leander Jedamus
# modifiziert Dienstag, 10. März 2020 11:32 von Leander Jedamus

from __future__ import print_function
import logging
import matrizen

import sys
if int(sys.version_info.major) < 3:
  my_input = raw_input
else:
  my_input = input

logger = logging.getLogger(__name__)

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
  inp = my_input('n = ')
  if inp.isdigit():
    n = int(inp)
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

      j = my_input('Welches Bra (Eingangsvektor):')
      if j.isdigit():
        j = int(j)
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
        for i in range(power):
          if ket[i] != "":
            print(ket[i])

        k = my_input('Welches Ket (Ausgangsvektor):')
        if k.isdigit():
          k = int(k)
          ket[k-1] = ""
          z_vector = vector[ket_ind[k-1]]
          mat = matrizen.mat_mul(s_vector,z_vector,n)
          if logger.isEnabledFor(logging.DEBUG):
            logger.debug("bits = {bits:s}".format(bits=str(bits)))
            logger.debug("bits[{index:d}] = {bits:s}".format(index=ket_ind[k-1],bits=bits[ket_ind[k-1]]))
            logger.debug("{z_vector:s}".format(z_vector=z_vector))
            logger.debug("mat = {mat:s}".format(mat=str(mat)))
          for i in range(power):
            for j in range(power):
              matrix[i][j] += mat[i][j]
              
    logger.info("matrix = {matrix:s}".format(matrix=str(matrix)))
    return(matrix)

# vim:ai sw=2 sts=4 expandtab

