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
    #print(data)  # this is a bytearray type

    if data is not None:
        led.value = True
        print ("Read " + str(len(data)) + " bytes")

        # convert bytearray to string
        #data_string = ''.join([chr(b) for b in data])
        #print(data_string, end="")
        print(hex_dump(data))

        led.value = False


# Function to send AT command and retrieve response
def send_at_command(command):
    uart.write(command)  # Send the command
    time.sleep(1)  # Wait for the response to be available
    response = uart.read(100)  # Read up to 100 bytes of response
    if response is not None:
        #response = response.decode('ascii').strip()  # Decode bytes to string
        print(hex_dump(response))
    return response



# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)

led.direction = digitalio.Direction.OUTPUT

# busio.UART(tx, rx, ... baudrate=X)
#uart = busio.UART(board.GP0, board.GP1, baudrate=9600)
uart = busio.UART(board.GP4, board.GP5, baudrate=9600, bits=8, parity=None, stop=1)

#uart = busio.UART(board.GP4, board.GP5, baudrate=19200)
#uart = busio.UART(board.GP4, board.GP5, baudrate=38400)
#uart = busio.UART(board.GP4, board.GP5, baudrate=57600)

#uart = busio.UART(board.GP16, board.GP17, baudrate=9600)
#uart = busio.UART(board.GP16, board.GP17, baudrate=115200)

while True:
    #   uart.write(("AT\r\n").encode("ascii"))
    #    read_and_dump()
    #uart.write(("AT+ADDR?\r\n").encode("ascii"))
    read_and_dump()

# Example usage
#while True:
    #print("Sending AT command")
    #response = send_at_command(b'AT')
    #print(response)
    #time.sleep(2)
