#!/usr/bin/python
import gaugette.rotary_encoder
A_PIN = 3
B_PIN = 4
counter = 0
encoder = gaugette.rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
while True:
	delta = encoder.get_delta()
	if delta!=0:
		counter = counter + delta
		print int(counter/4)
