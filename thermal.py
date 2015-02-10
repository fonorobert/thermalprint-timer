#!venv/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.append('python-escpos')

from escposmod import *

from utility import linebreak, i18n


string = 'Fertőzőbb kőbányák tangóharmonikák szennyeződés műtők apanázs vakulásig gyilkosság trombitaművészek brácsák egymilliárd kócsagok kávédaráló mágikus támadó alakként görkorcsolyák délutáni kényelem legcsevegőbb. Borogatások vasút átkelő legeslegdühösebb Hermész sajtó fahéjfái múzeum indoeurópai holdvilág köpenyek kánkánok nem beszélek angolul bordás hatvány hetvennégy állami differenciálgeometria sárgállik melírozás. Ünnepnapok tüzel pakisztániak erdészek előleg antonimák agáig változók destruktív utcaseprők szürke gém fülesek látássá megszállottabb dodekaéder étlen pénzt hírnök ragadós esküvői ruha. '

chars = ['Á', 'á', 'É', 'é', 'Í', 'í', 'Ó', 'ó', 'Ú', 'ú', 'Ö', 'ö', 'Ü', 'ü', 'Ő', 'ő', 'Ű', 'ű']
charr = ['A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u', 'O', 'o', 'U', 'u', 'O', 'o', 'U', 'u']

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
