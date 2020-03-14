#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 07:37 (C) 2020 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 08:14 von Leander Jedamus

from __future__ import print_function
import re
import os
import sys
import logging

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
log.setLevel(logging.DEBUG)
# log.setLevel(logging.INFO)


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

  if log.isEnabledFor(logging.DEBUG):
    log.debug("line = " + line)

  if not has_n:
    # n auslesen
    if (re.match(reg_n,line)):
      if log.isEnabledFor(logging.DEBUG):
        log.debug("n gefunden")
        n = re.sub(reg_n,"\g<1>",line)
        if n.isdigit():
          n = int(n)
          has_n = True
          log.debug("n = " + str(n))
        else:
          log.error("n is not a decimal")
datei.close()

# vim:ai sw=2 sts=4 expandtab

