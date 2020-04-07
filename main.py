#!/usr/bin/env python3
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 12:26 (C) 2020 von Leander Jedamus
# modifiziert Mittwoch, 01. April 2020 16:45 von Leander Jedamus
# modifiziert Dienstag, 31. März 2020 20:51 von Leander Jedamus
# modifiziert Freitag, 20. März 2020 09:39 von Leander Jedamus
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
import re
import matrix_aus_datei as datei
import matrix_interaktiv as interaktiv
import matrix_create as mcreate

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
  if int(sys.version_info.major) < 3:
    trans.install(unicode=True)
  else:
    trans.install()
except IOError:
  logger.error("Fehler in gettext")
  def _(s):
    return s

logger = logging.getLogger(__name__)

def matrix_ausgeben(matrix, matname):
  if matname != "":
    logger.info("Writing file \"{matname:s}\" ...".format(matname=matname))
    try:
      datei = open(matname,"w")
      (s, z) = matrix.shape
      datei.write("[")
      for i in range(s):
        datei.write("[")
        for j in range(z):
          datei.write("{bit:d}".format(bit=matrix[i][j]))
          if ((j+1)<z):
            datei.write(",")
        datei.write("]")
        if ((i+1)<s):
          datei.write(",\n")
      datei.write("]\n")
      datei.close()
    except IOError as e:
      logger.fatal(e)
      exit(-1)

if __name__ == '__main__':
  parser = ArgumentParser(description = _("Create a matrix from input and output bits"))
  parser.add_argument("-f","--file", dest="filename", default="",
                      help=_("select file to read"))
  parser.add_argument("-m","--matrix", dest="matname", default="",
                      help=_("select matrix file to write"))
  parser.add_argument("-c","--create", dest="create", default="0",
                      help=_("create file to write"))
  filename = parser.parse_args().filename
  matname = parser.parse_args().matname
  create = parser.parse_args().create
  if(filename == ""):
    if logger.isEnabledFor(logging.DEBUG):
      logger.debug("interaktiv")
    matrix = interaktiv.matrix_interaktiv()
    matrix_ausgeben(matrix, matname)
    print("matrix = {matrix:s}".format(matrix=str(matrix)))
  else:
    if(create != "0"):
      if not re.match(r"[-+]*\d+",create):
        print(_("Wrong create!"))
      else:
        n = int(create)
        if ((n<1) | (n>16)):
          print(_("Wrong create!"))
        else:
          if logger.isEnabledFor(logging.DEBUG):
            logger.debug(_("creating \"{filename:s}\".".format(filename=filename)))
          mcreate.matrix_create(n,filename)
    else:
      if logger.isEnabledFor(logging.DEBUG):
        logger.debug(_("input from \"{filename:s}\".".format(filename=filename)))
      matrix = datei.matrix_aus_datei(filename)
      matrix_ausgeben(matrix, matname)
      print("matrix = {matrix:s}".format(matrix=str(matrix)))

# vim:ai sw=2 sts=4 expandtab

