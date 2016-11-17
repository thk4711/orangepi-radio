#!/usr/bin/python
import alsaaudio
import time
#m = alsaaudio.Mixer('MIC2 boost AMP gain control')
m = alsaaudio.Mixer(control='Software', id=0, cardindex=1)
m.setvolume(10)
time.sleep(2)
m.setvolume(100)
