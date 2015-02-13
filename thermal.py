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
running = False

rem_lock = threading.Lock()
run_lock = threading.Lock()
e_running = threading.Event()


class TimerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def setremaining(self, value):
        global rem_lock
        with rem_lock:
            global remaining
            remaining = value

    def getremaining(self):
        global remaining
        return remaining

    def getrunning(self):
        global running
        return running

    def run(self):
        remaining = self.getremaining()
        while remaining > 0:
            if e_running.isSet():
                self.setremaining(remaining - 1)
                remaining = self.getremaining()
                time.sleep(1)
            else:
                time.sleep(1)
        with run_lock:
            global running
            running = False
        return

t = TimerThread()
t.setDaemon(True)
t.start()


def getremaining():
        global remaining
        return remaining


def setremaining(value):
        global rem_lock
        with rem_lock:
            global remaining
            remaining = value


def getrunning():
    global running
    return running


def timerstart():
    global e_running
    e_running.set()
    global running
    global run_lock
    with run_lock:
        running = True


def timerstop():
    global e_running
    e_running.clear()
    global running
    global run_lock
    with run_lock:
        running = False


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

@app.route('/timer', methods = ['GET', 'POST'])
def api_timer():
    if request.method == 'GET':
        resp = jsonify(remaining=getremaining(), running=getrunning())
        resp.status_code = 200
        return resp

    if request.method == 'POST':
        data = request.json

        if data['action'] == 'stop':
            timerstop()
        elif data['action'] == 'start':
            if 'remaining' in data:
                setremaining(data['remaining'])
                timerstart()
            else:
                timerstart()
        elif data['action'] == 'set':
            setremaining(data['remaining'])

        resp = jsonify(operation='succesful')
        resp.status_code = 200
        return resp


if __name__ == '__main__':
    app.run(debug=True)
