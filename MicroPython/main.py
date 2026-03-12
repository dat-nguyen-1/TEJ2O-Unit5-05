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

    def get_distance_mm(self):
        spi.init(
            baudrate=125000,
            sclk=self.sclk_pin,
            mosi=self.trigger_pin,
            miso=self.echo_pin,
        )
        pre = 0
        post = 0
        k = -1
        length = 500
        resp = bytearray(length)
        resp[0] = 0xFF
        spi.write_readinto(resp, resp)

        # find first non zero value
        try:
            i, value = next((ind, v) for ind, v in enumerate(resp) if v)
        except StopIteration:
            i = -1

        if i > 0:
            pre = bin(value).count("1")

            # find first non full high value afterwards
            try:
                k, value = next(
                    (ind, v)
                    for ind, v in enumerate(resp[i : length - 2])
                    if resp[i + ind + 1] == 0
                )
                post = bin(value).count("1") if k else 0
                k = k + i
            except StopIteration:
                i = -1
        dist = -1 if i < 0 else round(((pre + (k - i) * 8 + post) * 8 * 0.172) / 2)

        return dist

    def get_distance_cm(self):
        return self.get_distance_mm() * 0.1


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
