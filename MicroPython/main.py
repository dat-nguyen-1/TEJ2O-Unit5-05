"""
Created by: Dat Nguyen
Created on: Mar 2026
This module will calculate distance from the sonar.
"""

from microbit import *


class HCSR04:
    """
    This class abstracts out the functionality of the HC-SR04 and
    returns distance in mm
    Trigger: pin 1
    Echo: pin 2
    Serial clock: pin 13
    """

    def __init__(self, trigger_pin=pin1, echo_pin=pin2, sclk_pin=pin13):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.sclk_pin = sclk_pin

        spi.init(
            baudrate=125000,
            sclk=self.sclk_pin,
            mosi=self.trigger_pin,
            miso=self.echo_pin,
        )

    def get_distance_cm(self) -> int:
        pre = 0
        post = 0
        length = 500
        response = bytearray(length)
        response[0] = 0xFF
        spi.write_readinto(response, response)

        # find first non zero value
        index_start = -1
        for idx in range(length):
            if response[idx]:
                index_start = idx
                break
        if index_start == -1:
            return -1

        # find first zero value after ping
        index_end = -1
        for idx in range(index_start + 1, length):
            if response[idx] == 0:
                index_end = idx
                break
        if index_end < 0:
            return -1

        # count bits
        if index_start > 0:
            pre = bin(response[index_start]).count("1")
        if index_end >= 0:
            post = bin(response[index_end]).count("1")

        return round(((pre + (index_end - index_start) * 8 + post) * 8 * 0.0344) * 0.5)


# create sonar instance
sonar = HCSR04(trigger_pin=pin1, echo_pin=pin2, sclk_pin=pin13)

# initialize display
display.clear()
display.show(Image.HAPPY)

# main loop
while True:
    if button_a.was_pressed():
        # display distance
        distance = sonar.get_distance_cm()
        display.clear()
        display.scroll(str(distance) + " cm")

        # reset display
        display.clear()
        display.show(Image.HAPPY)
