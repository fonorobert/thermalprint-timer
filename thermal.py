#!venv/bin/python

import sys
sys.path.append('python-escpos')
from escpos import *
import threading
import time
#from utility import linebreak

from flask import Flask, request, jsonify

Epson = printer.Usb(0x04b8, 0x0e15)

remaining = 60


class TimerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def setglobal(self, value):
        global remaining
        remaining = value

    def getglobal(self):
        global remaining
        return remaining

    def run(self):
        remaining = self.getglobal()
        while remaining > 0:
            self.setglobal(remaining - 1)
            remaining = self.getglobal()
            #print(self.getglobal())
            time.sleep(1)
        return


def getremaining():
        global remaining
        return remaining


def stringlist(string, sep='|||'):
    if string is None:
        return None
    else:
        return string.split(sep)


def linebreak(string, charlimit=48):
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


def _print_text(string, width=48):
    printable = linebreak(string, width)
    if isinstance(printable, basestring):
        Epson.text(printable)
    else:
        for line in printable:
            Epson.text(line)
            Epson.control('LF')


def _print_img(imgpath):
    Epson.image(imgpath)
    Epson.control('LF')


def print_header(string, imgpath=None, string2=False, border="=*=|", width=48):
    Epson.set(align="center", font="A")
    Epson.text(border*(width/len(border)))
    Epson.control('LF')

    if imgpath:
        _print_img(imgpath)

    _print_text(string)

    if isinstance(string2, basestring):
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


def print_body(string):
    Epson.set(align="left", font="A", width=2, height=2)

    _print_text(string, width=48)

    Epson.set(align="center", font="A", width=1, height=1)


def print_footer(string, string2=False, border="=", width=48):
    Epson.control('LF')
    Epson.set(align="center", font="A")
    Epson.control('LF')

    Epson.text(border*(width/len(border)))
    Epson.control('LF')

    _print_text(string)

    if isinstance(string2, basestring):
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


app = Flask(__name__)
t = TimerThread()


@app.route('/printer', methods=['POST'])
def api_printer():
    data = request.json

    if 'header' in data:
        header = data['header']
    else:
        header = False
    if 'body' in data:
        body = data['body']
    else:
        body = False
    if 'footer' in data:
        footer = data['footer']
    else:
        footer = False

    if header:
        if 'text2' in header:
            print_header(header['text'], string2=stringlist(header['text2']),
                         imgpath='img/darpa-logo.gif')
        else:
            print_header(header['text'], imgpath='img/darpa-logo.gif')

    print_body(body)
    print_body(str(getremaining()))

    if footer:
        if 'text2' in footer:
            print_footer(footer['text'], string2=stringlist(footer['text2']))
        else:
            print_footer(footer['text'])

    Epson.cut()

    resp = jsonify(operation='succesful')
    resp.status_code = 200
    return resp

t.setDaemon(True)
t.start()

if __name__ == '__main__':
    app.run(debug=True)
