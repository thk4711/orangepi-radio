#!/usr/bin/python
import smbus
import time

capabilities  = {
                "volume"    : True,
                "bass"      : False,
                "mid"       : False,
                "treble"    : False,
                }

i2c = smbus.SMBus(0)

PT2257_ADDR = 0x44        # Chip address
EVC_OFF     = 0b11111111  # Function OFF (-79dB)
EVC_2CH_1   = 0b11010000  # 2-Channel, -1dB/step
EVC_2CH_10  = 0b11100000  # 2-Channel, -10dB/step
EVC_L_1     = 0b10100000  # Left Channel, -1dB/step
EVC_L_10    = 0b10110000  # Left Channel, -10dB/step
EVC_R_1     = 0b00100000  # Right Channel, -1dB/step
EVC_R_10    = 0b00110000  # Right Channel, -10dB/step
EVC_MUTE    = 0b01111000  # 2-Channel MUTE

def i2c_write(b):
    print "data: %x" % b
    try:
        i2c.write_byte(PT2257_ADDR, b)  # send data via i2c
    except Exception:
        pass

def evc_level(dB):
    if dB > 79:
        dB=79
    b = dB//10          # get the most significant digit (eg. 79 gets 7)
    a = dB%10           # get the least significant digit (eg. 79 gets 9)
    b = b & 0b0000111   # limit the most significant digit to 3 bit (7)
    return (b<<4) | a   # //return both numbers in one byte (0BBBAAAA)

def evc_setVolume(dB):
    bbbaaaa = evc_level(dB)
    aaaa    = bbbaaaa & 0b00001111
    bbb     = (bbbaaaa>>4) & 0b00001111
    #i2c_write(EVC_2CH_10 | bbb)
    #i2c_write(EVC_2CH_1 | aaaa)
    i2c.write_byte_data(PT2257_ADDR, EVC_2CH_10 | bbb, EVC_2CH_1 | aaaa)


def evc_setVolumeLeft(dB):
    bbbaaaa = evc_level(dB)
    aaaa    = bbbaaaa & 0b00001111
    bbb     = (bbbaaaa>>4) & 0b00001111
    i2c_write(EVC_L_10 | bbb)
    i2c_write(EVC_L_1 | aaaa)

def evc_setVolumeRight(dB):
    bbbaaaa = evc_level(dB)
    aaaa    = bbbaaaa & 0b00001111
    bbb     = (bbbaaaa>>4) & 0b00001111
    i2c_write(EVC_R_10 | bbb)
    i2c_write(EVC_R_1 | aaaa)

def init():
    time.sleep(0.5)
    masterVolume(50)

# ser volume in rage from 0 to 1000
def masterVolume(mv):
    mv = 79 - int(((mv * 79) / 100));
    evc_setVolume(mv)

# mute off
def muteOff():
    i2c_write(EVC_MUTE | (0 & 0b00000001))

# mute off
def muteOn():
    i2c_write(EVC_MUTE | (1 & 0b00000001))
