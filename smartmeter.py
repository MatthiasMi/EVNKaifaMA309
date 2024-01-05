#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .\smartmeter.py
"""
@author: Matthias
@version: 0.0.1
"""

from bs4 import BeautifulSoup
from datetime import datetime
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from gurux_dlms.GXDLMSTranslatorMessage import GXDLMSTranslatorMessage
import serial

### Start of Config ###
# Input your EVN Key (32 hex characters): "666857B666758CF6662166675F13C666"
evn_key = "666857B666758CF6662166675F13C666"  # <- intentionally incorrect

# Switches/Toggles (True | False)
o = True  # Log/Output
if o: print(f"Hello EVN, I'm {evn_key} - R U alive?")

### Start of Logic ###
gxdlmstr = GXDLMSTranslator()
gxdlmstr.blockCipherKey = GXByteBuffer(evn_key)
gxdlmstr.comments = True
comport = "/dev/ttyUSB0" # Config/Init

ser = serial.Serial(port=comport, baudrate=2400, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)

curtime = str(datetime.now())
if o: print(f"Hello EVN - reading data (~3 seconds) on{curtime}")

data = ser.read(size=282).hex()
if o: print("Hello EVN - data read.\n\ndata:\n=====")
if o: print(data)

msg = GXDLMSTranslatorMessage()
msg.message = GXByteBuffer(data)
gxbb = GXByteBuffer()
gxdlmstr.completePdu = True
markup = ""
while gxdlmstr.findNextFrame(msg, gxbb):
    gxbb.clear()
    markup += gxdlmstr.messageToXml(msg)

bs = BeautifulSoup(markup, "html.parser")

uints32 = str(bs.find_all("uint32"))
uints16 = str(bs.find_all("uint16"))
if o: print("uints16", uints16); print("uints32", uints32)
