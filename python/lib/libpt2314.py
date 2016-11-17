#!/usr/bin/python

import smbus
import time

i2c = smbus.SMBus(1)
i2c_address = 0x44

toneAttenuation =  [-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
toneValues      =  [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,14,14,13,13,12,12,11,11,10,10,9,9,8,8]

BASS_TONE_CONTROL      = 0x60
TREBLE_TONE_CONTROL    = 0x70

current_left_volume    = 0
current_left_volume    = 0
current_channel        = 0
current_tone_mode      = True

# Arduino like map function
def amap(x, in_min, in_max, out_min, out_max):
    result = (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    return result

# initialize PT2322
def init():
    time.sleep(0.5)  # in case this is first time - I2C bus not ready for this long on power on with 10uF cref
    muteOff()
    leftVolume(100)
    rightVolume(100)
    masterVolume(50)
    bass(50)
    treble(50)

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
def writeI2CChar(b):
    print "data: %x" % b
    try:
        i2c.write_byte(i2c_address, b)  # send data via i2c
    except Exception:
        pass

# helper
def updateAudioSwitch():
    global current_channel
    global current_tone_mode
    audioByte = 0b01000000 # audio switch + gain +11.25dB.
    if current_tone_mode:
        audioByte = audioByte | 0x00
    else:
        audioByte = audioByte | 0x04
    audioByte = audioByte | current_channel
    writeI2CChar(audioByte)

# tone on
def toneOn():
    global current_tone_mode
    current_tone_mode = 0x00
    updateAudioSwitch()

# tone off
def toneOff():
    global current_tone_mode
    current_tone_mode = 0x04
    updateAudioSwitch()

def switch_channel(channel):
    global current_channel
    if current_channel < 4 and current_channel > -1:
        current_channel = channel
        updateAudioSwitch()

# mute on
def muteOn():
    writeI2CChar(0b11011111)
    writeI2CChar(0b11111111)

# mute off
def muteOff():
    global current_right_volume
    global current_left_volume
    writeI2CChar(0b11000000 | current_right_volume)
    writeI2CChar(0b11000000 | current_left_volume)

#range : 0 to -15dB
def leftVolume(flv):
    global current_left_volume
    flv = amap(flv,0,100,0b00011111,0b00000000)
    writeI2CChar(0b11000000 | flv)
    current_left_volume = flv

#range : 0 to -15dB
def rightVolume(frv):
    global current_right_volume
    frv = amap(frv,0,100,0b00011111,0b00000000)
    writeI2CChar(0b11100000 | frv)
    current_right_volume = frv

#range : 0 to 63
def masterVolume(mv):
    mv = 63 - int(((mv * 63) / 100));
    writeI2CChar(mv)
    current_volume = mv

#range : +14 to -14dB, 2dB step
def bass(tb):
    tb = amap(tb,0,100,-14,14)
    tbv = toneLookup(tb)
    writeI2CChar(BASS_TONE_CONTROL | tbv)

#range : +14 to -14dB, 2dB step
def treble(tt):
    tt = amap(tt,0,100,-14,14)
    ttv = toneLookup(tt)
    writeI2CChar(TREBLE_TONE_CONTROL | ttv)
