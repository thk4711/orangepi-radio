#!/usr/bin/python
import wiringpi
import time

INPUT   = 0
OUTPUT  = 1
LOW     = 0
HIGH    = 1
PUD_UP  = 2

clk_pin = 4
dt_pin  = 5

wiringpi.wiringPiSetup()
wiringpi.pinMode(clk_pin,INPUT)
wiringpi.pullUpDnControl(clk_pin,PUD_UP)
wiringpi.pinMode(dt_pin,INPUT)
wiringpi.pullUpDnControl(dt_pin,PUD_UP)

encoderPos = 0
encoderPinALast = LOW
n = LOW

while True:
	n = wiringpi.digitalRead(clk_pin)
	if ((encoderPinALast == LOW) and (n == HIGH)):
		if(wiringpi.digitalRead(dt_pin) == LOW):
			encoderPos = encoderPos + 1
		else:
			encoderPos = encoderPos - 1
		print encoderPos
	encoderPinALast = n
	time.sleep(0.003)
