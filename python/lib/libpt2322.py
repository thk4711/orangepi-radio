#!/usr/bin/python

import smbus
import time

i2c = smbus.SMBus(1)
i2c_address = 0x44          # i2c address for PT2322

i2c_pcf8574 = 0x20          # i2c address of IO chip
io_port = 0b00000000        # binary number for pcf8574 i2c IO IC

toneAttenuation =  [-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
toneValues      =  [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15]

FL_VOLUME_CONTROL      = 0x10
FR_VOLUME_CONTROL      = 0x20
CENTER_VOLUME_CONTROL  = 0x30
RL_VOLUME_CONTROL      = 0x40
RR_VOLUME_CONTROL      = 0x50
SUB_VOLUME_CONTROL     = 0x60
FUNCTION_SELECT        = 0x70
BASS_TONE_CONTROL      = 0x90
MIDDLE_TONE_CONTROL    = 0xa0
TREBLE_TONE_CONTROL    = 0xb0
INPUT_SW_ACTIVE        = 0xc7
MASTER_VOLUME_1STEP    = 0xd0
MASTER_VOLUME_10STEP   = 0xe0
SYSTEM_RESET           = 0xff
MUTE_ON                = 0x08
_3D_OFF                = 0x04
TONE_DEFEAT            = 0x02
function               = 0

class inputs:
    RASPI = 0
    AUX   = 1
    USB   = 2

def amap(x, in_min, in_max, out_min, out_max):
    result = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    #print result
    return result


# initialize PT2322
def init():
    global function
    time.sleep(0.5)          # in case this is first time - I2C bus not ready for this long on power on with 10uF cref
    function = _3D_OFF       #mute OFF, 3D OFF, tone control ON
    masterVolumeValue = 50   #master volume = -15db - temporary at 0
    bassValue   = 0x07       #Bass   = -0dB
    middleValue = 0x07       #Middle = -0dB
    trebleValue = 0x07       #Treble = -0dB

    # initialize device
    writeI2CChar(SYSTEM_RESET)
    writeI2CChar(INPUT_SW_ACTIVE)   # required to activate

    # set the trim volumes to zero
    writeI2CChar(FL_VOLUME_CONTROL)       #0db
    writeI2CChar(FR_VOLUME_CONTROL)       #0db
    writeI2CChar(CENTER_VOLUME_CONTROL)   #0db
    writeI2CChar(RL_VOLUME_CONTROL)       #0db
    writeI2CChar(RR_VOLUME_CONTROL)       #0db
    writeI2CChar(SUB_VOLUME_CONTROL)      #0db

    # set the master voume
    tmp = MASTER_VOLUME_1STEP  | (HEX2BCD(masterVolumeValue) &  0x0f)
    writeI2CChar(tmp)
    tmp = MASTER_VOLUME_10STEP | ((HEX2BCD(masterVolumeValue)  &  0xf0)>>4)
    writeI2CChar(tmp)

    # set default function
    writeI2CChar(FUNCTION_SELECT | function)

    # and finish with the tone controls
    writeI2CChar(BASS_TONE_CONTROL | bassValue)
    writeI2CChar(MIDDLE_TONE_CONTROL | middleValue)
    writeI2CChar(TREBLE_TONE_CONTROL | trebleValue)
    switch_input(inputs.RASPI)

# tone table lookup
def toneLookup(tone):
    # print"looking for: " + str(tone)
    for i in range(0, len(toneAttenuation)):
        if (toneAttenuation[i] == tone):
            # print"returning: " + str(toneValues[i])
            return toneValues[i]
    # default if given an invalid value
    return 7

# helper method
def HEX2BCD(x):
    y = (x / 10) << 4
    y = y | (x % 10)
    return (y)

# helper method
def writeI2CChar(b):
    #time.sleep(0.1)
    print "data: %x" % b
    try:
        i2c.write_byte(i2c_address, b)  # send data via i2c
    except Exception:
        pass

# mute on
def muteOn():
    global function
    function = function | MUTE_ON
    writeI2CChar(FUNCTION_SELECT | function)

# mute off
def muteOff():
    global function
    function  = function & (0x0f - MUTE_ON)
    writeI2CChar(FUNCTION_SELECT | function)

# 3D on
def _3DOn():
    global function
    function  = function & (0x0f - _3D_OFF)
    writeI2CChar(FUNCTION_SELECT | function)

# 3D off
def _3DOff():
    global function
    function = function | _3D_OFF
    writeI2CChar(FUNCTION_SELECT | function)

# tone on
def toneOn():
    global function
    function  = function & (0x0f - TONE_DEFEAT)
    writeI2CChar(FUNCTION_SELECT | function)

# tone off
def toneOff():
    global function
    function = function | TONE_DEFEAT
    writeI2CChar(FUNCTION_SELECT | function)

#range : 0 to -15dB
def leftVolume(flv):
    flv = amap(flv,0,100,-15,0)
    writeI2CChar(FL_VOLUME_CONTROL | -flv)

#range : 0 to -15dB
def rightVolume(frv):
    frv = amap(frv,0,100,-15,0)
    writeI2CChar(FR_VOLUME_CONTROL | -frv)

#range : 0 to -15dB
def centerVolume(cv):
    cv = amap(cv,0,100,-15,0)
    writeI2CChar(CENTER_VOLUME_CONTROL | -cv)

#range : 0 to -15dB
def rearLeftVolume(rlv):
    rlv = amap(rlv,0,100,-15,0)
    writeI2CChar(RL_VOLUME_CONTROL | -rlv)

#range : 0 to -15dB
def rearRightVolume(rrv):
    rrv = amap(rrv,0,100,-15,0)
    writeI2CChar(RR_VOLUME_CONTROL | -rrv)

#range : 0 to -15dB
def subwooferVolume(sv):
    sv = amap(sv,0,100,-15,0)
    writeI2CChar(SUB_VOLUME_CONTROL | -sv)

#range : 0 to -79dB
def masterVolume(mv):
    mv = amap(mv,0,100,-79,0)
    writeI2CChar(MASTER_VOLUME_1STEP  | (HEX2BCD(-mv)   &  0x0f))
    writeI2CChar(MASTER_VOLUME_10STEP | ((HEX2BCD(-mv)  &  0xf0)>>4))

#range : +14 to -14dB, 2dB step
def bass(tb):
    tb = amap(tb,0,100,-14,14)
    tbv = toneLookup(tb)
    writeI2CChar(BASS_TONE_CONTROL | tbv)

#range : +14 to -14dB, 2dB step
def middle(tm):
    tm = amap(tm,0,100,-14,14)
    tmv = toneLookup(tm)
    writeI2CChar(MIDDLE_TONE_CONTROL | tmv)

#range : +14 to -14dB, 2dB step
def treble(tt):
    tt = amap(tt,0,100,-14,14)
    ttv = toneLookup(tt)
    writeI2CChar(TREBLE_TONE_CONTROL | ttv)

#switch the relais acording to the current app mode
def switch_input(inp):
    if inp == inputs.RASPI:
        i2c.write_byte(i2c_pcf8574,0b00000000)
    if inp == inputs.AUX:
        i2c.write_byte(i2c_pcf8574,0b00000001)
    if inp == inputs.USB:
        i2c.write_byte(i2c_pcf8574,0b00000011)
