/* Copyright (c) 2020 MTHS All rights reserved
 *
 * Created by: Dat Nguyen
 * Created on: Mar 2026
 * This program calculate the distance in front of the micro:bit.
*/

// Intialize variables
let distance: number = 0

// Intialize display
basic.showIcon(IconNames.Happy)

input.onButtonPressed(Button.A, function() {
    // Calculate distance from sonar
    distance = sonar.ping(DigitalPin.P1, DigitalPin.P2, PingUnit.Centimeters)

    // Display distan                                             ce
    basic.clearScreen()
    basic.showString(distance.toString() + " cm")

    // Reset display
    basic.showIcon(IconNames.Happy)
})
