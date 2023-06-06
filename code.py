# Simple code to read a message from the Dabble App over the DSDTech HM-10 bluetooth module
# Author: Eric Z. Ayers <ericzundel@gmail.com>

"""CircuitPython Example of how to read data from the Dabble app"""
import binascii
import board
import busio
import digitalio
import time

class Dabble():
    def __init__(self, tx_pin, rx_pin):
        # busio.UART(tx, rx, ... baudrate=X)
        self._uart = busio.UART(tx_pin, rx_pin, baudrate=9600, bits=8, parity=None, stop=1, timeout=.05)

    def hex_dump(data):
        hex_str = binascii.hexlify(data).decode()
        hex_dump_str = ''
        for i in range(0, len(hex_str), 2):
            hex_dump_str += hex_str[i:i+2] + ' '
            if (i + 2) % 64 == 0:
                hex_dump_str += '\n'
        return hex_dump_str

    def read_message(self):
        data = self._uart.read(8)
        if (data is None):
            return None

        if (len(data) != 8):
            print("Expected 8 bytes, got %d" % len(data))
            return None

        if (data[0] != 0xff and data[7] != 0x00):
            print("expected 0xFF at head and 0x00 at end")
            return None

        button_data = data[5]
        direction_data = data[6]
        return DabbleGameMessage(button_data, direction_data)

class DabbleGameMessage():

    def __init__(self, button_data, direction_data):
        self._button_data = button_data
        self._direction_data = direction_data

    @property
    def start_pressed(self):
        return self._button_data & 0x01

    @property
    def select_pressed(self):
        return self._button_data & 0x02

    @property
    def triangle_pressed(self):
        return self._button_data & 0x04

    @property
    def circle_pressed(self):
        return self._button_data & 0x08

    @property
    def cross_pressed(self):
        return self._button_data & 0x10

    @property
    def square_pressed(self):
        return self._button_data & 0x20

    @property
    def up_arrow_pressed(self):
        return self._direction_data & 0x01

    @property
    def down_arrow_pressed(self):
        return self._direction_data & 0x02

    @property
    def left_arrow_pressed(self):
        return self._direction_data & 0x04

    @property
    def right_arrow_pressed(self):
        return self._direction_data & 0x08

    @property
    def no_direction_pressed(self):
        return self._direction_data == 0x00

    @property
    def no_action_pressed(self):
        return self._button_data == 0x00

    def __str__(self):

        result = ""

        if self.no_action_pressed:
            result += "NO_ACTION "

        if self.select_pressed:
            result += "SELECT "
        if self.start_pressed:
            result += "START "
        if self.triangle_pressed:
            result += "TRIANGLE "
        if self.circle_pressed:
            result += "CIRCLE "
        if self.cross_pressed:
            result += "CROSS "
        if self.square_pressed:
            result += "SQUARE "

        if self.no_direction_pressed:
            result += "NO_DIRECTION "
        if self.up_arrow_pressed:
            result += "UP "
        if self.left_arrow_pressed:
            result += "LEFT "
        if self.down_arrow_pressed:
            result += "DOWN "
        if self.right_arrow_pressed:
            result += "RIGHT "


        return result

dabble = Dabble(board.GP0, board.GP1)

while True:
    message = dabble.read_message()
    if (message != None):
        print("Message: " + str(message))
        # Implement tank steering on a 2 wheeled robot
        if (message.up_arrow_pressed):
            print("Move both motors forward")
        elif (message.down_arrow_pressed):
            print("Move both motors backward")
        elif (message.right_arrow_pressed):
            print("Move left motor forward and right motor backward")
        elif (message.left_arrow_pressed):
            print("Move left motor backward and right motor forward")
        elif (message.no_direction_pressed):
            print("Stop both motors")
        else:
            print("Something Crazy happened with direction!")
