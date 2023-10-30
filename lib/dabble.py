# Simple code to read a message from the Dabble App over the DSDTech HM-10 bluetooth module
# Author: Eric Z. Ayers <ericzundel@gmail.com>

"""CircuitPython module to parse data from the Dabble app connected to an HM-10 bluetooth module"""
import binascii
import board
import busio
import digitalio
import time

def _hex_dump(data):
    hex_str = binascii.hexlify(data).decode()
    hex_dump_str = ''
    for i in range(0, len(hex_str), 2):
        hex_dump_str += hex_str[i:i+2] + ' '
        if (i + 2) % 64 == 0:
            hex_dump_str += '\n'
    return hex_dump_str

class Dabble():
    def __init__(self, tx_pin, rx_pin, debug=False):
        # busio.UART(tx, rx, ... baudrate=X)
        self._uart = busio.UART(tx_pin, rx_pin, baudrate=9600, bits=8, parity=None, stop=1, timeout=.05)
        self._debug = debug

    def hex_dump(self, data):
        _hex_dump(data)

    def debug_msg(self, message):
        if (self._debug):
            print(message)

    def read_message(self):
        """Returns a DabbleMessage on success, None if there is no message to read."""
        data = self._uart.read(8)
        if (data is None):
            return None

        if (len(data) != 8):
            self.debug_msg("Expected 8 bytes, got %d" % len(data))
            return None

        if (data[0] != 0xff and data[7] != 0x00):
            self.debug_msg("Expected 0xFF at head and 0x00 at end")
            return None

        module_type = data[1]
        if (module_type != 0x01):
            print("Dabble library only supports Gamepad module on UI. Got: " + _hex_dump(data))
            return None

        function_type = data[2]
        if (data[2] != 0x01): # Game controller type
            print("Dabble library only supports Digital Controller type. Got: " + _hex_dump(data))
            return None

        button_data = data[5]
        direction_data = data[6]
        return DabbleGamepadMessage(function_type, button_data, direction_data)

class DabbleMessage():
    """A base class for message returned from the Dabble App"""
    def __init__(self, message_type):
        self._message_type = message_type

    @property
    def message_type(self):
        return self._message_type

class DabbleGamepadMessage(DabbleMessage):
    """Message returned when the Dabble App is in Game Controller Mode"""

    def __init__(self, gamepad_mode, button_data, direction_data):
        super().__init__("DabbleGamepadMessage")
        self._gamepad_mode = gamepad_mode
        self._button_data = button_data
        self._direction_data = direction_data

    @property
    def mode(self):
        if (self._gamepad_mode is 0x01):
            return "DIGITAL"
        elif (self._gamepad_mode is 0x02):
            return "ANALOG"
        elif (self._gamepad_mode is 0x03):
            return "ACCL"
        else:
            return "UNKNOWN"

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
        result = f"{self.message_type}: "

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
