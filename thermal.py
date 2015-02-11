#!venv/bin/python

import sys
sys.path.append('python-escpos')
import argparse
from escpos import *
from utility import linebreak

parser = argparse.ArgumentParser()


# config = configparser.ConfigParser()
# config.read('config.txt')


# string = config['test']['string']

# chars = config['i18n']['chartable']
# noacc = config['i18n']['noaccents']
# hexac = config['i18n']['hexaccent']




# # for line in lines:
# #     print line
# # exit(0)


Epson = printer.Usb(0x04b8, 0x0e15)
Epson.set(align="center", font="A")


def _print_text(string, width=48):
    printable = linebreak(string, width)
    if isinstance(printable, str):
        Epson.text(printable)
    else:
        for line in printable:
            Epson.text(line)
            Epson.control('LF')


def _print_img(imgpath):
    Epson.image(imgpath)
    Epson.control('LF')


def print_header(string, imgpath=None, string2=False, border="=*=|", width=48):
    Epson.text(border*(width/len(border)))
    Epson.control('LF')

    _print_img(imgpath)

    _print_text(string)

    if isinstance(string2, str):
        Epson.control('LF')
        Epson.control('LF')
        _print_text(string2)
    elif isinstance(string2, list):
        Epson.control('LF')
        Epson.control('LF')
        for line in string2:
            _print_text(line)
            Epson.control('LF')

    Epson.control('LF')
    Epson.text(border*(width/len(border)))
    Epson.control('LF')
    Epson.control('LF')
    Epson.control('LF')
    Epson.control('LF')


def print_body(string):
    Epson.set(align="left", font="A", width=2, height=2)
    _print_text(string, width=48)
    Epson.set(align="center", font="A")


def print_footer(string, string2=False, border="=", width=48):
    Epson.control('LF')
    Epson.control('LF')

    Epson.text(border*(width/len(border)))
    Epson.control('LF')

    _print_text(string)

    if isinstance(string2, str):
        Epson.control('LF')
        Epson.control('LF')
        _print_text(string2)
    elif isinstance(string2, list):
        Epson.control('LF')
        Epson.control('LF')
        for line in string2:
            _print_text(line)
            Epson.control('LF')

    Epson.control('LF')
    Epson.text(border*(width/len(border)))
    Epson.control('LF')
    Epson.control('LF')
    Epson.control('LF')


#======================================
#Testing calls
#======================================

string4 = "Fertozobb kobanyak tangoharmonikak szennyezodes mutok apanazs vakulasig gyilkossag trombitamuveszek bracsak egymilliard kocsagok kavedaralo magikus tamado alakkent gorkorcsolyak delutani kenyelem legcsevegobb. Borogatasok vasut atkelo legeslegduhosebb Hermesz sajto fahejfai muzeum indoeuropai holdvilag kopenyek kankanok nem beszelek angolul bordas hatvany hetvennegy allami differencialgeometria sargallik melirozas."

helpstring = 'Nyissatok ki az aktataskat. Onnantol mar konnyu lesz.'

stringlong = 'Remaining time: 0 months 0 days 0 hours 43 minutes'

stringshort = 'Project PROMETHEUS'

footerstring = 'www.trap.hu'

lineslist = ['Time until impact:', '0 months 0 days 0 hours 43 minutes']

numberlines = 'abcd efgh ijkl mnop qrst uvwx yz abcd efgh ijkl mnop qrst uvwx yz abcd efgh ijkl mnop qrst uvwx yz abcd efgh ijkl mnop qrst uvwx yz'


print_header(stringshort, 'img/darpa-logo.gif', string2=lineslist)
print_body(helpstring)
print_footer(footerstring)
Epson.cut()
