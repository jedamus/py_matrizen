#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 12:26 (C) 2020 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 13:29 von Leander Jedamus

from __future__ import print_function
from argparse import ArgumentParser
import gettext
import os
import sys
import logging
import logging.config
import atexit
import time
import log
import matrix_aus_datei as datei
import matrix_interaktiv as interaktiv

home = os.environ["HOME"]
user = os.environ["USER"]
log_path_and_filename = os.path.join("/tmp",user + "matrizen.log")
logger = ""
atexit.register(logging.shutdown)

logging.Formatter.converter=time.gmtime
logging._srcFile=None
logging.logThreads=0
logging.logProcesses=0
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

"""
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
"""

scriptpath = os.path.abspath(os.path.dirname(sys.argv[0]))
try:
  trans = gettext.translation("matrizen",os.path.join(scriptpath, "translate"))
  trans.install(unicode=True)
except IOError:
  print("name = " + __name__)
  logger.error("Fehler in gettext")
  def _(s):
    return s

if __name__ == '__main__':
  logger = logging.getLogger(__name__)
  parser = ArgumentParser(description = _("Create a matrix from input and output bits"))
  parser.add_argument("-f","--file", dest="filename", default="",
                      help=_("select file"))
  filename = parser.parse_args().filename
  if(filename == ""):
    if logger.isEnabledFor(logging.DEBUG):
      logger.debug("interaktiv")
    matrix = interaktiv.matrix_interaktiv()
  else:
    if logger.isEnabledFor(logging.DEBUG):
      logger.debug(_("input from \"{filename:s}\".".format(filename=filename)))
    matrix = datei.matrix_aus_datei(filename)
  print("matrix = {matrix:s}".format(matrix=matrix))

# vim:ai sw=2 sts=4 expandtab

