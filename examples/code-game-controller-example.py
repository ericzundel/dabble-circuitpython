# Simple code to read a message from the Dabble App over the DSDTech HM-10 bluetooth module
# Author: Eric Z. Ayers <ericzundel@gmail.com>

"""CircuitPython Example of how to read data from the Dabble app"""
import binascii
import board
import busio
import digitalio
import time

from dabble import Dabble

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