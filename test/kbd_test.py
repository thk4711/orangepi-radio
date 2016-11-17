#!/usr/bin/env python

from evdev import InputDevice, categorize, ecodes, list_devices
lirc_device = InputDevice('/dev/input/event5')
import time

#-----------------------------------------------------------------#
#             translate key code to string                        #
#-----------------------------------------------------------------#
def key_code_to_string(code):
    if code == 103: return "KEY_UP"
    elif code == 108: return "KEY_DOWN"
    elif code == 105: return "KEY_LEFT"
    elif code == 106: return "KEY_RIGHT"
    elif code == 28:  return "KEY_ENTER"
    elif code == 127: return "KEY_MENU"
    elif code == 1: return "KEY_PLAYPAUSE"
    print code


#-----------------------------------------------------------------#
#                 background thred to get keycode                 #
#-----------------------------------------------------------------#
def keypressd(lirc_device):
    global key_code
    event_type  = ""
    repeat_cout = 0

    for event in lirc_device.read_loop():
        if event.type == ecodes.EV_KEY:
            print(str(event))
            string = str(event)
            if "val 01" in string: event_type = "DOWN"
            if "val 02" in string: event_type = "REPEAT"
            if "val 00" in string: event_type = "UP"
            if event_type == "DOWN":
                key_code = key_code_to_string(event.code)
            if event_type == "REPEAT":
                repeat_cout = repeat_cout +1
                if repeat_cout > 4:
                    key_code = key_code_to_string(event.code)
            if event_type == "UP":
                if repeat_cout > 4:
                    key_code = None
                repeat_cout = 0


while True:
    keypressd(lirc_device)
    #for event in InputDevice('/dev/input/event0').read_loop():
        #if event.type == ecodes.EV_KEY:
        #print(str(event))
    #time.sleep(0.1)
    #for event in InputDevice('/dev/input/event1').read_loop():
        #if event1.type == ecodes.EV_KEY:
        #print(str(event))
