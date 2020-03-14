#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 07:37 (C) 2020 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 08:33 von Leander Jedamus

from __future__ import print_function
import re
import matrizen
import os
import sys
import logging


logger_path_and_filename = os.path.join("/tmp","matrizen.logger")
file_handler = logging.FileHandler(logger_path_and_filename)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s",
                              "%d.%m.%Y %H:%M:%S")
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)


datei = open("matrix_xor.dat","r")
reg_comment = re.compile(r"^#.*")
reg_empty = re.compile(r"^$")
reg_n = re.compile(r"n = (\d+)")

has_n = False
for line in datei:
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
        logger.debug("n gefunden")
      n = re.sub(reg_n,"\g<1>",line)
      if n.isdigit():
        n = int(n)
        has_n = True
        logger.debug("n = " + str(n))
        (bits,vector) = matrizen.bits_and_vector(n)
        logger.debug("bits = " + str(bits))
        logger.debug("vector = " + str(vector))
      else:
        logger.fatal("n is not a decimal")
  else:
    pass

datei.close()

# vim:ai sw=2 sts=4 expandtab

