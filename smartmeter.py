#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .\smartmeter.py
"""
@author: Matthias
@version: 0.0.3
"""

from bs4 import BeautifulSoup
from datetime import datetime
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from gurux_dlms.GXDLMSTranslatorMessage import GXDLMSTranslatorMessage
import serial

def hexstr2int(uints, index, width=4):
    """ `hexstr2int` converts hex string `uints` starting at `index` with `width` to `int`."""
    return int(str(uints)[index:index+width],16)


### Start of Config ###

# Switches/Toggles (True | False)
o = True  # Log/Output
useFILE = True  # write `html`

# Paths Config/Init
comport = "/dev/ttyUSB0"
html = "/var/www/html/index.html"

# Input your EVN Key (32 hex characters): "666857B666758CF6662166675F13C666"
evn_key = "666857B666758CF6662166675F13C666"  # <- intentionally incorrect
if o: print(f"Hello EVN, I'm {evn_key} - R U alive?")

### Start of Logic ###
gxdlmstr = GXDLMSTranslator()
gxdlmstr.blockCipherKey = GXByteBuffer(evn_key)
gxdlmstr.comments = True

ser = serial.Serial(port=comport, baudrate=2400, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)

tries=0  # Number of failed attempts
while 1:
    timestamp = str(datetime.now())
    if o: print(f"Hello EVN - reading data (~3 seconds) on{timestamp}")
    
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

    width=4 # uints16
    # Voltage L 1,2,3 in [V]
    voltageL1 = hexstr2int(uints16, 16, width)/10
    voltageL2 = hexstr2int(uints16, 48, width)/10
    voltageL3 = hexstr2int(uints16, 80, width)/10

    # Vurrent L 1,2,3 in [A]
    currentL1 = hexstr2int(uints16, 112, width)/100
    currentL2 = hexstr2int(uints16, 144, width)/100
    currentL3 = hexstr2int(uints16, 176, width)/100

    factor = hexstr2int(uints16, 208, width)/1000
    
    width*=2 # uints32
    # Energy A+/- in [Wh] -> [kWh]
    energyP = hexstr2int(uints32, 16,width)/1000
    energyN = hexstr2int(uints32, 52, width)/1000

    # Power P+/- in [W]
    powerP = hexstr2int(uints32, 88, width)
    powerN = hexstr2int(uints32, 124, width)
    powerD = powerP-powerN

    s = ""
    st = f"power  : {powerD:.0f} [W],\n"; s+=st
    if o: print(st)
    st = f"consume: {energyP:.2f} [KWh],\n"; s+=st
    if o: print(st)
    st = f"supply : {energyN:.2f} [KWh],\n"; s+=st
    if o: print(st)
    st = f"L1 : {voltageL1:.2f} [V], {currentL1:.2f} [A],\n"; s+=st
    if o: print(st)
    st = f"L2 : {voltageL2:.2f} [V], {currentL2:.2f} [A],\n"; s+=st
    if o: print(st)
    st = f"L3 : {voltageL3:.2f} [V], {currentL3:.2f} [A].\n"; s+=st
    if o: print(st)
    st = f"powerN : {powerN:.2f} [W],\n"; s+=st
    if o: print(st)
    st = f"powerD : {powerD:.2f} [W],\n"; s+=st
    if o: print(st)
    st = f"data timestamp: {timestamp}"; s+=st
    if o: print(st)
    
    if useFILE:
        if o: print(f"[HTML] Writing data to '{html}'\n")
        f = open(html, "w")
        f.write("<html><head><title>Smartmeter</title><meta http-equiv=\"refresh\" content=\"3\"></head></html><pre>\n")
        f.write(s)
        f.close()
        