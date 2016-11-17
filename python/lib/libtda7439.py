#!/usr/bin/python

import smbus
import time

i2c = smbus.SMBus(1)
i2c_address = 0x44

# Sub addresses
TDA7439_input_sel  = 0x00
TDA7439_input_gain = 0x01
TDA7439_volume     = 0x02
TDA7439_bass       = 0x03
TDA7439_middle     = 0x04
TDA7439_trebble    = 0x05
TDA7439_ratt       = 0x06
TDA7439_latt       = 0x07
TDA7439_mute       = 0x38

# Input selection
TDA7439_input_1    = 0x03
TDA7439_input_2    = 0x02
TDA7439_input_3    = 0x01
TDA7439_input_4    = 0x00

# define some lookup tables
toneInput = [-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7]
toneValue = [0,1,2,3,4,5,6,7,14,13,12,11,10,9,8]

volInput  = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
volValue  = [56,40,32,24,16,8,7,6,5,4,3,2,1,0]

attnInput = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
attnValue = [120,72,64,56,48,40,32,24,16,8,7,6,5,4,3,2,1,0]

current_volume = 0

# Arduino like map function
def amap(x, in_min, in_max, out_min, out_max):
    result = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    return result

# do some initial settings
def init():
    time.sleep(0.5)
    set_attn(100)
    set_gain(0)
    masterVolume(50)
    bass(50)
    middle(50)
    trebble(50)
    switch_channel(1)

# table lookup
def Lookup(value,xinput,xvalue):
    # print"looking for: " + str(tone)
    for i in range(0, len(xinput)):
        if (xinput[i] == value):
            # print"returning: " + str(toneValues[i])
            return xvalue[i]
    # default if given an invalid value
    return xvalue[5]

# change input channel
def switch_channel(channel):
    value = TDA7439_input_1
    if channel == 1:   value = TDA7439_input_1
    elif channel == 2: value = TDA7439_input_2
    elif channel == 3: value = TDA7439_input_3
    elif channel == 4: value = TDA7439_input_4
    sendi2c(TDA7439_input_sel,value)

# set master volume
def masterVolume(volume):
    global current_volume
    current_volume = volume
    volume = amap(volume,0,100,0,13)
    volume = Lookup(volume, volInput, volValue)
    #volume = 8
    sendi2c(TDA7439_volume,volume)

# set speaker attenuation
def set_attn(attn):
    attn = amap(attn,0,100,0,17)
    attn = Lookup(attn, attnInput, attnValue)
    #attn = 0
    sendi2c(TDA7439_ratt,attn)
    sendi2c(TDA7439_latt,attn)

# set input gain(gain)
def set_gain(gain):
    gain = amap(gain,0,100,0,15)
    #gain = 0
    sendi2c(TDA7439_input_gain,gain)

# mute on
def muteOn():
    sendi2c(TDA7439_volume,TDA7439_mute)

# mute off
def muteOff():
    masterVolume(current_volume)

# bass control
def bass(level):
    level = amap(level,0,100,-7,7)
    level = Lookup(level, toneInput, toneValue)
    sendi2c(TDA7439_bass,level)

# midd control
def middle(level):
    level = amap(level,0,100,-7,7)
    llevel = Lookup(level, toneInput, toneValue)
    sendi2c(TDA7439_middle,level)

# trebble control
def trebble(level):
    level = amap(level,0,100,-7,7)
    level = Lookup(level, toneInput, toneValue)
    sendi2c(TDA7439_trebble,level)

# send data over i2c
def sendi2c(a,b):
    print "data: " + str(a) + " - " + str(b)
    try:
        i2c.write_byte_data(i2c_address, a, b) # send command with i2c
    except Exception:
        pass
