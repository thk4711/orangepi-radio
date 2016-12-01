#!/usr/bin/env python

from   evdev import InputDevice, categorize, ecodes, list_devices
import thread
import time
from   select import select
import wiringpi

INPUT        = 0
OUTPUT       = 1
LOW          = 0
HIGH         = 1
PUD_UP       = 2

A_1_PIN      = 23            # 1st pin of 1st encoder
B_1_PIN      = 22            # 2nd pin of 1st encoder
BTN_1_PIN	 = 24			 # button of 1st encoder

A_2_PIN      = 5             # 1st pin of 2nd encoder
B_2_PIN      = 4             # 2nd pin of 2nd encoder
BTN_2_PIN	 = 11			 # button of 2nd encoder

POWER_PIN	 = 21			 # desired power state

key_code            = None

encoder1Pos         = 0
last_encoder1Pos    = 0
encoder1PinALast    = LOW
last_button_1_state = HIGH

encoder2Pos         = 0
last_encoder2Pos    = 0
encoder2PinALast    = LOW
last_button_2_state = HIGH

lirc_device = InputDevice('/dev/input/event5')

Power_State = "ON"

#-----------------------------------------------------------------#
#       get the steps from encoder since last asked               #
#-----------------------------------------------------------------#
def get_delta_1():
	global encoder1Pos
	global last_encoder1Pos
	diff = encoder1Pos - last_encoder1Pos
	if diff != 0:
		last_encoder1Pos = encoder1Pos
	return(diff)

#-----------------------------------------------------------------#
#             check encoder fore movement                         #
#-----------------------------------------------------------------#
def read_encoder_1():
    global encoder1Pos
    global encoder1PinALast
    n = wiringpi.digitalRead(A_1_PIN)
    if ((encoder1PinALast == LOW) and (n == HIGH)):
        if(wiringpi.digitalRead(B_1_PIN) == LOW):
            encoder1Pos = encoder1Pos + 1
    	else:
            encoder1Pos = encoder1Pos - 1
    encoder1PinALast = n

def read_encoder_2():
	global encoder2Pos
	global encoder2PinALast
	global key_code
	n = wiringpi.digitalRead(A_2_PIN)
	if ((encoder2PinALast == LOW) and (n == HIGH)):
		if(wiringpi.digitalRead(B_2_PIN) == LOW):
			#encoder2Pos = encoder2Pos + 1
			key_code = "KEY_UP"
		else:
			#encoder2Pos = encoder2Pos - 1
			key_code = "KEY_DOWN"
		#print encoder2Pos
	encoder2PinALast = n

def read_button_1():
	global last_button_1_state
	global key_code
	n = wiringpi.digitalRead(BTN_1_PIN)
	if (n != last_button_1_state):
		if (n == LOW):
			key_code = "KEY_MENU"
		last_button_1_state = n

def read_button_2():
	global last_button_2_state
	global key_code
	n = wiringpi.digitalRead(BTN_2_PIN)
	if (n != last_button_2_state):
		if (n == LOW):
			key_code = "KEY_PLAYPAUSE"
		last_button_2_state = n

def read_power_button():
	global Power_State
	n = wiringpi.digitalRead(POWER_PIN)
	if (n == LOW):
		Power_State = "ON"
	else:
		Power_State = "OFF"

def encoder_loop():
	while True:
		read_encoder_1()
		read_encoder_2()
		read_button_1()
		read_button_2()
		read_power_button()
		time.sleep(0.003)

#-----------------------------------------------------------------#
#             set key code to enter                               #
#-----------------------------------------------------------------#
def switch_pressed(message):
    global key_code
    if message == 7:
        key_code = "KEY_ENTER"

#-----------------------------------------------------------------#
#             translate key code to string                        #
#-----------------------------------------------------------------#
def key_code_to_string(code):
    if code == 103: return "KEY_UP"
    if code == 108: return "KEY_DOWN"
    if code == 105: return "KEY_LEFT"
    if code == 106: return "KEY_RIGHT"
    if code == 28:  return "KEY_ENTER"
    if code == 139: return "KEY_MENU"
    if code == 164: return "KEY_PLAYPAUSE"
    # print code

#-----------------------------------------------------------------#
#                 background thred to get keycode                 #
#-----------------------------------------------------------------#
def keypressd(lirc_device):
    global key_code
    event_type  = ""
    repeat_cout = 0

    for event in lirc_device.read_loop():
        if event.type == ecodes.EV_KEY:
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

#-----------------------------------------------------------------#
#                       read encoder                              #
#-----------------------------------------------------------------#
def readLeftRight(min_value, max_value, current_value, ir_value):
	delta = 0
	enc_delta = 0
	new_value = current_value
	if ir_value == "KEY_LEFT":
		delta = - 1
	if ir_value == "KEY_RIGHT":
		delta = + 1
	encoder_delta = 2 * get_delta_1()
	new_value = current_value + encoder_delta + delta
	if (new_value > max_value):
		new_value = max_value
	if (new_value < min_value):
		new_value = min_value
	return new_value

#-----------------------------------------------------------------#
#                       read lirc socket                          #
#-----------------------------------------------------------------#
def read_key():
    global key_code
    result = ""
    if key_code != None:
        result = key_code
        key_code = None
    return result

#-----------------------------------------------------------------#
#                      start some things                          #
#-----------------------------------------------------------------#
def init():
	print(lirc_device)
	wiringpi.wiringPiSetup()
	wiringpi.pinMode(A_1_PIN,INPUT)
	wiringpi.pullUpDnControl(A_1_PIN,PUD_UP)
	wiringpi.pinMode(B_1_PIN,INPUT)
	wiringpi.pullUpDnControl(B_1_PIN,PUD_UP)
	wiringpi.pinMode(BTN_1_PIN,INPUT)
	wiringpi.pullUpDnControl(BTN_1_PIN,PUD_UP)

	wiringpi.pinMode(A_2_PIN,INPUT)
	wiringpi.pullUpDnControl(A_2_PIN,PUD_UP)
	wiringpi.pinMode(B_2_PIN,INPUT)
	wiringpi.pullUpDnControl(B_2_PIN,PUD_UP)
	wiringpi.pinMode(BTN_2_PIN,INPUT)
	wiringpi.pullUpDnControl(BTN_2_PIN,PUD_UP)

	wiringpi.pinMode(POWER_PIN,INPUT)
	wiringpi.pullUpDnControl(POWER_PIN,PUD_UP)

	thread.start_new_thread(encoder_loop, ())
	thread.start_new_thread(keypressd, (lirc_device, ))
