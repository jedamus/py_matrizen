#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Dienstag, 10. März 2020 10:55 (C) 2020 von Leander Jedamus
# modifiziert Montag, 16. März 2020 13:25 von Leander Jedamus
# modifiziert Sonntag, 15. März 2020 15:07 von Leander Jedamus
# modified Sunday, 15. March 2020 07:17 by Leander Jedamus
# modifiziert Samstag, 14. März 2020 14:15 von Leander Jedamus
# modified Saturday, 14. March 2020 14:13 by Leander Jedamus
# modifiziert Samstag, 14. März 2020 13:25 von Leander Jedamus
# modifiziert Mittwoch, 11. März 2020 17:35 von Leander Jedamus
# modifiziert Dienstag, 10. März 2020 11:32 von Leander Jedamus

from __future__ import print_function
import logging
import matrizen
import re
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

def input_number(n1,n2,output):
  while(True):
    try:
      inp = my_input(output)
    except KeyboardInterrupt:
      print()
      exit(-1)
    if not re.match(r"[-+]*\d+",inp):
      print(_("Wrong input!"))
    else:
      n = int(inp)
      if ((n >= n1) and (n <= n2)):
        break
      else:
        print(_("Wrong input!"))
  return(n)

def ask_vector(power,bits,output,modify):
  while(True):
    for i in range(power):
      if bits[i] != "":
        print(bits[i])

    j = input_number(1,power,output)
    if bits[j-1] == "":
      print(_("Wrong input!"))
    else:
      if modify:
        bits[j-1] = ""
      break

  return(j)

def matrix_interaktiv():
  debug_enabled = logger.isEnabledFor(logging.DEBUG)
  n = input_number(1,13,"n = ")
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
  ket = []
  for i in range(power):
    bra.append("{i:d}. {bra:s}".format(i=i+1,bra=bits[i]))
    ket.append("{i:d}. {ket:s}".format(i=i+1,ket=bits[i]))
  bras = power
  while(bras > 0):
    j = ask_vector(power,bra,_('Wich bra (input vector):'),True)
    if debug_enabled:
      logger.debug("bits = {bits:s}".format(bits=bits))
      logger.debug("bits[{index:d}] = {bits:s}".format(index=j-1,bits=bits[j-1]))
    bras -= 1
    s_vector = vector[j-1]
    if debug_enabled:
      logger.debug("s_vector = {s_vector:s}".format(s_vector=s_vector))

    k = ask_vector(power,ket,_('Wich Ket (output vector):'),False)
    z_vector = vector[k-1]
    mat = matrizen.mat_mul(s_vector,z_vector,n)
    if debug_enabled:
      logger.debug("bits = {bits:s}".format(bits=bits))
      logger.debug("bits[{index:d}] = {bits:s}".format(index=k-1,bits=bits[k-1]))
      logger.debug("z_vector = {z_vector:s}".format(z_vector=z_vector))
      logger.debug("mat = {mat:s}".format(mat=mat))

    for i in range(power):
      for j in range(power):
        matrix[i][j] += mat[i][j]
              
  logger.debug("matrix = {matrix:s}".format(matrix=matrix))
  return(matrix)

# vim:ai sw=2 sts=4 expandtab

