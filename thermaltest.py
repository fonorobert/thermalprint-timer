#!/usr/bin/python3
import sys
sys.path.append('python-escpos')

from escposmod import *

Epson = printer.Usb(0x04b8, 0x0e15)
Epson.set(align="center", font="A", char='int')
Epson.control('LF')
Epson.control('LF')

Epson.image('logo.png')

Epson.control('LF')
Epson.control('LF')
Epson.control('LF')
Epson.control('LF')
Epson.cut()
