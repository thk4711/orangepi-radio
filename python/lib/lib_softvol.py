#!/usr/bin/python
import alsaaudio

capabilities  = {
    "volume"    : True,
    "bass"      : False,
    "mid"       : False,
    "treble"    : False
    }

app_modes = {
    "RAD"  : True,
    "AIR"  : True,
    "SPOT" : True,
    "AUX"  : False,
    "USB"  : False
    }

# init the alsa software mixer
def init():
    global mixer
    mixer = alsaaudio.Mixer(control='Software', id=0, cardindex=1)

# sets volume in rage from 0 to 1000
def masterVolume(mv):
    mixer.setvolume(mv)

# mute on
def muteOn():
    mixer.setvolume(0)

# just a dummy in that module
def muteOff():
    return

# just a dummy in that module
def bass(x):
    return

# just a dummy in that module
def middle(x):
    return

# just a dummy in that module
def treble(x):
    return

# just a dummy in that module
def switch_input(x):
    return
