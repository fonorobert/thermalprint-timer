#!/usr/bin/env python3

from subprocess import call

call(['git', 'submodule update'])
call(['virtualenv', 'venv -p python3.4'])
call(['./venv/bin/pip', 'install Pillow'])
call(['pyusb/setup.py', 'install'])
