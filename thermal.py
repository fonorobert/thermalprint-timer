#!/usr/bin/python
#venv/bin/python3
import sys
sys.path.append('python-escpos')

from escposmod import *

import configparser

config = configparser.ConfigParser()
config.read('config.txt')


string = config['test']['string']

# chars = config['i18n']['chartable']
# noacc = config['i18n']['noaccents']
# hexac = config['i18n']['hexaccent']

# list = linebreak(string)
# lines = []
# for chunk in list:
#     lines.append(i18n(chunk, chars, charr))

# # for line in lines:
# #     print line
# # exit(0)


# Epson = printer.Usb(0x04b8, 0x0e15)
# Epson.set(align="center", font="A", char='int')
# Epson.control('LF')
# Epson.control('LF')

# for line in lines:
#     Epson.text(line)
#     Epson.control('LF')
# Epson.control('LF')
# Epson.control('LF')
# Epson.control('LF')
# Epson.control('LF')
# Epson.control('LF')
# Epson.control('LF')

# Epson.cut()


class Printer:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.txt')
        self.chars = config['i18n']['chartable']
        self.noacc = config['i18n']['noaccents']
        self.hexac = config['i18n']['hexaccent']
        self.imgdef = config['defaults']['imgpath']
        self.Epson = printer.Usb(0x04b8, 0x0e15)
        self.Epson.set(align="center", font="A", char='int')

    def linebreak(self, string, charlimit=48):
        if len(string) < charlimit:
            return string
        else:
            words = string.split(' ')
            chunks = ['']
            for word in words:
                if chunks == [] or len(chunks[-1])+len(word) > charlimit:
                    chunks.append(word + ' ')
                else:
                    chunks[-1] += word + ' '
            return chunks

    def i18n(self, string, chars, charcodes):
        for char in chars:
            string = string.replace(char, charcodes[chars.index(char)])
        return string

    def print_text(self, text, accent=False):
        list = self.linebreak(text)
        lines = []
        if accent is True:
            for chunk in list:
                lines.append(self.i18n(chunk, self.chars, self.hexac))
        elif accent is False:
            for chunk in list:
                lines.append(self.i18n(chunk, self.chars, self.noacc))

        for line in lines:
            self.Epson.text(line)
            self.Epson.control('LF')

    def print_img(self, imgpath='default'):
        if imgpath is 'default':
            imgpath = self.imgdef
        self.Epson.image(imgpath)
        self.Epson.control('LF')

printer = Printer()
printer.print_text(string)
printer.print_img(imgpath='img/logo.jpg')
#printer.print_img()
