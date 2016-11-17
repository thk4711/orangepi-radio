#!/usr/bin/python

import time, signal, sys
from Adafruit_ADS1x15 import ADS1x15

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

ADS1115 = 0x01	# 16-bit ADC

# Select the gain
gain = 4096  # +/- 4.096V
sps = 860    # 860 samples per second

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
adc = ADS1x15(ic=ADS1115)

def read_button_1():
    button = 0
    volts = adc.readADCSingleEnded(0, gain, sps) / 1000
    if volts > 2.9:
        button = 0
    elif volts < 0.2:
        button = 1
    elif volts > 0.4 and volts < 0.8:
        button = 2
    elif volts > 0.9 and volts < 1.2:
        button = 3
    elif volts > 1.3 and volts < 1.6:
        button = 4
    elif volts > 1.8 and volts < 2.1:
        button = 5
    return button

def read_button_2():
    button = 0
    volts = adc.readADCSingleEnded(1, gain, sps) / 1000
    if volts > 3:
        button = 0
    elif volts < 0.2:
        button = 6
    elif volts > 0.4 and volts < 0.9:
        button = 7
    elif volts > 1.1 and volts < 1.6:
        button = 8
    elif volts > 1.7 and volts < 2.1:
        button = 9
    elif volts > 2.2 and volts < 2.6:
        button = 10
    return button

def read_button_3():
    button = 0
    volts = adc.readADCSingleEnded(2, gain, sps) / 1000
    if volts > 3:
        button = 0
    elif volts < 0.2:
        button = 11
    elif volts > 0.4 and volts < 0.8:
        button = 12
    elif volts > 0.9 and volts < 1.3:
        button = 13
    elif volts > 1.4 and volts < 1.7:
        button = 14
    elif volts > 1.9 and volts < 2.1:
        button = 15
    elif volts > 2.2 and volts < 2.6:
        button = 16
    return button


def get_voltage():
    volts_1 = adc.readADCSingleEnded(0, gain, sps) / 1000
    volts_2 = adc.readADCSingleEnded(1, gain, sps) / 1000
    volts_3 = adc.readADCSingleEnded(2, gain, sps) / 1000
    return(volts_1, volts_2, volts_3)

def test():
    (v1, v2, v3) = get_voltage()
    print "%.6f" % (v1) + " " + "%.6f" % (v2) + " " + "%.6f" % (v3)
    time.sleep(0.3)

def buttons():
    result = 0
    button = read_button_1()
    if button > 0:
        time.sleep(0.01)
        button = read_button_1()
        if button > 0:
            result = button
    button = read_button_2()
    if button > 0:
        time.sleep(0.01)
        button = read_button_2()
        if button > 0:
            result = button
    button = read_button_3()
    if button > 0:
        time.sleep(0.01)
        button = read_button_3()
        if button > 0:
            result = button
    return result

while True:
    test()
    key = buttons()
    if key:
        print key
