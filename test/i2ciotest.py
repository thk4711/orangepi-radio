#!/usr/bin/python
from smbus import SMBus
from time import sleep

bus = SMBus(1) # Port 1 used on REV2

io_port = 0b00000000

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

while True:
    io_port = set_bit(io_port,0)
    bus.write_byte(0x20,io_port)
    sleep(2)
    io_port = clear_bit(io_port,0)
    bus.write_byte(0x20,io_port)
    sleep(2)
