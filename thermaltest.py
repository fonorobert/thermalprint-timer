#!venv/bin/python
import sys
sys.path.append('python-escpos')

from escpos import *

Epson = printer.Usb(0x04b8, 0x0e15)
Epson.set(align="center", font="A")
Epson.control('LF')
Epson.control('LF')

Epson.image('logo.png')

Epson.control('LF')
Epson.control('LF')
Epson.control('LF')
Epson.control('LF')
Epson.cut()
