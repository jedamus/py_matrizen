#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Dienstag, 10. März 2020 10:55 (C) 2020 von Leander Jedamus
# modifiziert Donnerstag, 19. November 2020 09:14 von Leander Jedamus
# modifiziert Mittwoch, 29. April 2020 12:50 von Leander Jedamus
# modifiziert Samstag, 11. April 2020 15:16 von Leander Jedamus
# modifiziert Donnerstag, 09. April 2020 06:56 von Leander Jedamus
# modifiziert Dienstag, 31. März 2020 19:58 von Leander Jedamus
# modifiziert Freitag, 20. März 2020 09:43 von Leander Jedamus
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
import re
import sys
import os
import inspect
import gettext
import numpy as np
import matrizen

if int(sys.version_info.major) < 3:
  my_input = raw_input
else:
  my_input = input

logger = logging.getLogger(__name__)

scriptpath = os.path.realpath(os.path.abspath(os.path.split( \
               inspect.getfile(inspect.currentframe()))[0]))
try:
  trans = gettext.translation("matrizen",os.path.join(scriptpath, "locale"))
  if int(sys.version_info.major) < 3:
    trans.install(unicode=True)
  else:
    trans.install()
except IOError:
  logger.error("Fehler in gettext")
  def _(s):
    return s

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
  n = input_number(1,16,"n = ")

  bits = matrizen.get_bits(n)

  power = 2**n
  matrix = np.zeros( (power,power), dtype=np.int8 )
  s_vector = np.zeros( (power,1), dtype=np.int8 )
  z_vector = np.zeros( (1,power), dtype=np.int8 )

  # bra und ket einlesen
  bra = []
  ket = []
  for i in range(power):
    bra.append("{i:d}. {bra:s}".format(i=i+1,bra=bits[i]))
    ket.append("{i:d}. {ket:s}".format(i=i+1,ket=bits[i]))

  bras = power
  while(bras > 0):
    j = ask_vector(power,bra,_("Wich bra (input vector):"),True)
    if debug_enabled:
      logger.debug("bits = {bits:s}".format(bits=str(bits)))
      logger.debug("bits[{index:d}] = {bits:s}".format(index=j-1,bits=bits[j-1]))

    bras -= 1
    s_vector[j-1][0] = 1
    if debug_enabled:
      logger.debug("s_vector = {s_vector:s}".format(s_vector=str(s_vector)))

    k = ask_vector(power,ket,_("Wich Ket (output vector):"),False)
    z_vector[0][k-1] = 1

    mat = s_vector*z_vector

    if debug_enabled:
      logger.debug("bits = {bits:s}".format(bits=str(bits)))
      logger.debug("bits[{index:d}] = {bits:s}".format(index=k-1,bits=bits[k-1]))
      logger.debug("z_vector = {z_vector:s}".format(z_vector=str(z_vector)))
      logger.debug("mat = {mat:s}".format(mat=str(mat)))

    s_vector[j-1][0] = 0
    z_vector[0][k-1] = 0

    matrix += mat
              
  logger.debug("matrix = {matrix:s}".format(matrix=str(matrix)))
  return(matrix)

# vim:ai sw=2 sts=4 expandtab

