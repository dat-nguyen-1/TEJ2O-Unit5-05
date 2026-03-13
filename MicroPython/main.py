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

        # Find first non zero value
        index_start = -1
        for idx in range(length):
            if response[idx]:
                index_start = idx
                break
        if index_start == -1:
            return -1

        # Find first zero value after ping
        index_end = -1
        for idx in range(index_start + 1, length):
            if response[idx] == 0:
                index_end = idx
                break
        if index_end < 0:
            return -1

        # Count bits
        if index_start > 0:
            pre = response[index_start].bit_count()
        if index_end >= 0:
            post = response[index_end].bit_count()

        return round(((pre + (index_end - index_start) * 8 + post) * 8 * 0.0172) / 2)


# Create sonar instance
sonar = HCSR04(trigger_pin=pin1, echo_pin=pin2, sclk_pin=pin13)

# Initialize display
display.clear()
display.show(Image.HAPPY)

# Main loop
while True:
    if button_a.was_pressed():
        # Display distance
        distance = sonar.distance_cm()
        display.clear()
        display.show(distance)
