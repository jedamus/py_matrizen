#!/home/leander/anaconda3/bin/python
# coding=utf-8 -*- python -*-

# erzeugt Freitag, 20. März 2020 16:50 (C) 2020 von Leander Jedamus
# modifiziert Freitag, 20. März 2020 16:58 von Leander Jedamus

from __future__ import print_function

zahl = 10 + 4j # komplexe Zahl

print("zahl = {zahl:.1f}".format(zahl=zahl))
print("zahl.real = {zahl:.1f}".format(zahl=zahl.real))
print("zahl.imag = {zahl:.1f}".format(zahl=zahl.imag))
print("zahl.conjugate() = {zahl:.1f}".format(zahl=zahl.conjugate()))

# vim:ai sw=2 sts=4 expandtab

