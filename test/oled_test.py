#!/usr/bin/env python

import time
from   lib import oled as display


display.disp_content.tonemode = "Vol"
display.disp_content.tonevalue = 50
display.disp_content.time = "17:55"
display.disp_content.name = "DRadio Wissen"
display.disp_content.artist = "Bla"
display.disp_content.title = "Blubber"
display.disp_content.app_mode = "RAD"
display.disp_content.source_string = 0
display.disp_content.wifi = 60
display.disp_content.volume = 50
display.disp_content.mpd_stat = "stop"

display.update_display(1234567)
time.sleep(2)

display.disp_content.tonemode = "Vol"
display.disp_content.tonevalue = 30
display.disp_content.time = "0:17"
display.disp_content.name = "Deutschlandfunk"
display.disp_content.artist = "Bla"
display.disp_content.title = "Blubber"
display.disp_content.app_mode = "SPOT"
display.disp_content.source_string = 0
display.disp_content.wifi = 10
display.disp_content.volume = 30
display.disp_content.mpd_stat = "play"

display.update_display(1234567)

count=100

while count >= 0:
    display.disp_content.tonevalue = count
    display.disp_content.volume = count
    display.disp_content.wifi = count
    display.update_display(1234567)
    count = count - 1
    time.sleep(0.2)

while count <= 100:
    display.disp_content.tonevalue = count
    display.disp_content.volume = count
    display.disp_content.wifi = count
    display.update_display(1234567)
    count = count + 1
    time.sleep(0.2)
