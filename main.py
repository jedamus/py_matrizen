#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 12:26 (C) 2020 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 12:43 von Leander Jedamus

from __future__ import print_function
from argparse import ArgumentParser
import gettext
import os
import sys
import logging
import log

home = os.environ["HOME"]
user = os.environ["USER"]
log_path_and_filename = os.path.join("/tmp",user + "matrizen.log")

file_handler = logging.FileHandler(log_path_and_filename)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s",
                              "%d.%m.%Y %H:%M:%S")
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

scriptpath = os.path.abspath(os.path.dirname(sys.argv[0]))
try:
  trans = gettext.translation("matrizen",os.path.join(scriptpath, "translate"))
  trans.install(unicode=True)
except IOError:
  logger.error("Fehler in gettext")
  def _(s):
    return s

if __name__ == '__main__':
  parser = ArgumentParser(description = _("Create a matrix from input and output bits"))
  parser.add_argument("-f","--file", dest="filename", default="matrix_cnot.dat",
                      help=_("select file"))
  filename = parser.parse_args().filename
  logger.debug("input from \"{filename:s}\".".format(filename=filename))

# vim:ai sw=2 sts=4 expandtab

