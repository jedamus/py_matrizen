#!/usr/bin/env python
# coding=utf-8 -*- python -*-

# erzeugt Samstag, 14. März 2020 07:37 (C) 2020 von Leander Jedamus
# modifiziert Donnerstag, 19. November 2020 09:14 von Leander Jedamus
# modifiziert Freitag, 05. Juni 2020 13:48 von Leander Jedamus
# modifiziert Donnerstag, 04. Juni 2020 08:04 von Leander Jedamus
# modifiziert Mittwoch, 29. April 2020 12:50 von Leander Jedamus
# modifiziert Mittwoch, 08. April 2020 09:05 von Leander Jedamus
# modifiziert Dienstag, 07. April 2020 17:34 von Leander Jedamus
# modifiziert Mittwoch, 01. April 2020 15:11 von Leander Jedamus
# modifiziert Dienstag, 31. März 2020 23:25 von Leander Jedamus
# modifiziert Freitag, 20. März 2020 09:41 von Leander Jedamus
# modifiziert Montag, 16. März 2020 13:18 von Leander Jedamus
# modifiziert Sonntag, 15. März 2020 14:21 von Leander Jedamus
# modified Sunday, 15. March 2020 06:55 by Leander Jedamus
# modifiziert Sonntag, 15. März 2020 06:53 von Leander Jedamus
# modifiziert Samstag, 14. März 2020 13:59 von Leander Jedamus

from __future__ import print_function
import re
import os
import inspect
import sys
import time
import copy
import logging
import gettext
import numpy as np
from numpy.linalg import inv
import threading
import queue

logger = logging.getLogger(__name__)

scriptpath = os.path.realpath(os.path.abspath(os.path.split( \
               inspect.getfile(inspect.currentframe()))[0]))
try:
  trans = gettext.translation("matrizen",os.path.join(scriptpath, "locale"))
# trans.install(unicode=True)
  trans.install()
except IOError:
  logger.error("Fehler in gettext")
  def _(s):
    return s

vector_save = None
matrix = None
worker_count = 4
time_count = 0
time_sum = 0.0

class calculate(threading.Thread):
  Lock = threading.Lock()
  Queue = queue.Queue()

  def run(self):
    global matrix
    global time_sum
    global time_count

    is_debug = logger.isEnabledFor(logging.DEBUG)

    while True:
      (s_index, z_index) = calculate.Queue.get()

      start_time = time.clock()

      temp_matrix = self.calc_the_matrix(s_index, z_index)

      calculate.Lock.acquire()

      matrix += temp_matrix

      end_time = time.clock()
      took_time = end_time - start_time
      time_count += 1
      time_sum += took_time

      if is_debug:
        logger.debug(_("Vector- and Matrix-operations took {time:1.2f} seconds").format(time=took_time))

      calculate.Lock.release()

      calculate.Queue.task_done()

  def calc_the_matrix(self, s_index, z_index):
    global vector_save

    s_vector = copy.deepcopy(vector_save).T
    s_vector[s_index][0] = 1
    z_vector = copy.deepcopy(vector_save)
    z_vector[0][z_index] = 1
    if logger.isEnabledFor(logging.DEBUG):
      logger.debug("vector_save = {vector_save:s}".format(vector_save=str(vector_save)))
      logger.debug("s_vector = {s_vector:s}".format(s_vector=str(s_vector)))
      logger.debug("z_vector = {z_vector:s}".format(z_vector=str(z_vector)))

    return(s_vector*z_vector)

def matrix_aus_datei(filename="matrix_cnot.dat"):
  global matrix
  global vector_save
  global worker_count
  global time_sum
  global time_count

  time_sum = 0.0
  time_count = 0

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
  reg_bits = re.compile(r"([01]+) > ([01xX]+)")
  reg_lbits = re.compile(r"([01]+) [01xX]+")
  reg_rbits = re.compile(r"[01]+ ([01xX]+)")

  has_n = False
  has_bits = []
  line_no = 0
  bits_count = 0
  is_first = True

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
        else:
          logger.fatal(_("n is not a decimal"))
    else:
      if is_first:
        is_first = False

        power = 2**n

        matrix = np.zeros( (power,power), dtype=np.int8 )
        vector_save = np.zeros( (1,power), dtype=np.int8 )

        for i in range(power):
          has_bits.append(False)

        worker_threads = [calculate() for i in range(worker_count)]
        i = 1
        for thread in worker_threads:
          logger.info(_("Started worker {i:d}.").format(i=i))
          i += 1
          thread.setDaemon(True)
          thread.start()

      if debug_enabled:
        logger.debug("vector_save = {vector_save:s}".format(vector_save=str(vector_save)))
      if (re.match(reg_bits,line)):
        if debug_enabled:
          logger.debug(_("found bits"))
        line = re.sub(reg_bits,"\g<1> \g<2>",line)
        lbits = re.sub(reg_lbits,"\g<1>",line)
        rbits = re.sub(reg_rbits,"\g<1>",line)
        if debug_enabled:
          logger.debug("lbits = " + lbits)
          logger.debug("rbits = " + rbits)

        ## new:
        for i in range(len(rbits)):
          if (rbits[i] == "x"):
            rbits = rbits.replace("x","0")
          elif (rbits[i] == "X"):
            rbits = rbits.replace("X","0")

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

            logger.debug("Before Queueing.")
            calculate.Queue.put((s_index, z_index))
            logger.debug("After Queueing.")
            logger.info("bits_count = {bits_count:d}".format(bits_count=bits_count))
      else:
        logger.fatal(_("Line {line_no:d} doesn't match").format(line_no=line_no))
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

  calculate.Queue.join()
  logger.debug("matrix = {matrix:s}".format(matrix=str(matrix)))
  logger.info(_("Average time vector- and matrix-operations took {time:1.4f} seconds").format(time=time_sum/time_count))
  try:
    m2 = inv(matrix)
    print("inv(matrix) = \n",m2)
  except np.linalg.LinAlgError:
    print("Matrix ist singulär!")
  return(matrix)

# vim:ai sw=2 sts=4 expandtab

