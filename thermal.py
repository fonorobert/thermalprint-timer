#!venv/bin/python3
# -*- coding: UTF-8 -*-
import sys
sys.path.append('python-escpos')

from escposmod import *

from utility import linebreak, i18n
import configparser

config = configparser.ConfigParser()
config.read('config.txt')


string = config['test']['string']

chars = config['i18n']['chartable']
charr = config['i18n']['noaccents']

list = linebreak(string)
lines = []
for chunk in list:
    lines.append(i18n(chunk, chars, charr))

# for line in lines:
#     print line
# exit(0)


Epson = printer.Usb(0x04b8, 0x0e15)
Epson.set(align="center", font="A", char='int')
Epson.control('LF')
Epson.control('LF')

for line in lines:
    Epson.text(line)
    Epson.control('LF')
Epson.control('LF')
Epson.control('LF')
Epson.control('LF')
Epson.control('LF')
Epson.control('LF')
Epson.control('LF')

Epson.cut()
