# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials UART Serial example"""
import board
import busio
import digitalio
import time

import binascii

def hex_dump(data):
    hex_str = binascii.hexlify(data).decode()
    hex_dump_str = ''
    for i in range(0, len(hex_str), 2):
        hex_dump_str += hex_str[i:i+2] + ' '
        if (i + 2) % 64 == 0:
            hex_dump_str += '\n'
    return hex_dump_str

def read_and_dump():
    data = uart.read(256)  # read up to 32 bytes

    if data is not None:
        print ("Read " + str(len(data)) + " bytes")
        print(hex_dump(data))


# busio.UART(tx, rx, ... baudrate=X)
tx_pin = board.GP0
rx_pin = board.GP1
uart = busio.UART(tx_pin, rx_pin, baudrate=9600, bits=8, parity=None, stop=1, timeout=.05)
#uart = busio.UART(board.GP4, board.GP5, baudrate=19200)
#uart = busio.UART(board.GP4, board.GP5, baudrate=38400)
#uart = busio.UART(board.GP4, board.GP5, baudrate=57600)

#uart = busio.UART(board.GP16, board.GP17, baudrate=9600)
#uart = busio.UART(board.GP16, board.GP17, baudrate=115200)

while True:
    read_and_dump()
