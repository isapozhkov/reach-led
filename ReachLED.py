#!/usr/bin/python

# ReachView code is placed under the GPL license.
# Written by Egor Fedorov (egor.fedorov@emlid.com)
# Copyright (c) 2015, Emlid Limited
# All rights reserved.

# If you are interested in using ReachView code as a part of a
# closed source project, please contact Emlid Limited (info@emlid.com).

# This file is part of ReachView.

# ReachView is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ReachView is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ReachView.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import time
from multiprocessing import Process
from GPIO import GPIO

class ReachLED(object):

    pwm_prefix = "/sys/class/pwm/pwmchip0/"

    def __init__(self):
        self.pins = [GPIO(12), GPIO(13), GPIO(182)]
 
        self.blinker_process = None

        self.colors_dict = {
            "off": [0, 0, 0],
            "red": [1, 0, 0],
            "green": [0, 1, 0],
            "blue": [0, 0, 1],
            "white": [1, 1, 1],
            "yellow": [1, 1, 0],
            "cyan": [0, 1, 1],
            "magenta": [1, 0, 1],
            "orange": [1, 0.4, 0],
            "weakred": [0.1, 0, 0]
        }

        self.pwm_channels = [0, 1, 2] # red, green, blue

        # first, we need to change the pin's pinmux to mode1
        for pin in self.pins:
            pin.setPinmux("mode1")

        # then, export the 3 pwn channels if needed
        for ch in self.pwm_channels:
            if not os.path.exists(self.pwm_prefix + "/pwm" + str(ch)):
                with open(self.pwm_prefix + "export", "w") as f:
                    f.write(str(ch))

        # enable all of the channels
        for ch in self.pwm_channels:
            with open(self.pwm_prefix + "pwm" + str(ch) + "/enable", "w") as f:
                f.write("1")

        # set period
        for ch in self.pwm_channels:
            with open(self.pwm_prefix + "pwm" + str(ch) + "/period", "w") as f:
                f.write("1000000")


    def setDutyCycle(self, channel, percentage=100):
        # 0% = 1000000
        # 100% = 0

        duty_value = (100 - percentage) * 10000

        with open(self.pwm_prefix + "pwm" + str(channel) + "/duty_cycle", "w") as f:
            f.write(str(duty_value))

    def setColor(self, color, power_percentage=100):
        if color in self.colors_dict.keys():
            for channel in self.pwm_channels:
                self.setDutyCycle(channel, self.colors_dict[color][channel] * power_percentage)
            return True
        else:
            return False

    def startBlinker(self, pattern, delay=0.5):
    	# pattern example: "red,blue,off"

	if pattern:
    	    for color in pattern.split(","):
    		if color not in self.colors_dict:
    		    return False
    	else:
    	    return False

    	if self.blinker_process is not None:
    	    self.stopBlinker()

        if self.blinker_process is None:
            self.blinker_process = Process(target = self.blinkPattern, args = (pattern, delay))
            self.blinker_process.start()
            return True

        return False

    def stopBlinker(self):
        if self.blinker_process is not None:
            self.blinker_process.terminate()
            self.blinker_process.join()
            self.blinker_process = None

    def blinkPattern(self, pattern, delay=0.5):
    	# pattern example: "red,blue,off"
        
        colors =  pattern.split(",")

    	while True:
            for color in colors:
                self.setColor(color)
                time.sleep(delay)

def test():
    led = ReachLED()
    print("Starting...")
    led.setDutyCycle(0, 0)

    time.sleep(1)
    print("After pause...")
    print("Channel 0")
    led.setDutyCycle(0, 100)
    time.sleep(1)
    print("Channel 1")
    led.setDutyCycle(0, 0)
    led.setDutyCycle(1, 100)
    time.sleep(1)
    print("Channel 2")
    led.setDutyCycle(1, 0)
    led.setDutyCycle(2, 100)
    time.sleep(1)

if __name__ == "__main__":
    test()
    led = ReachLED()

    if len(sys.argv) < 2:
        print "Usage: {} color".format(sys.argv[0])

        print "Colors:"
        for color in led.colors_dict.keys():
        	print "\t", color
    else:
        if not led.setColor(sys.argv[1]):
            print("Can't set this color. You may add this in the colors_dict variable.")








