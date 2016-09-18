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
from gpio import GPIO

class ReachLED(object):

    pwm_prefix = "/sys/class/pwm/pwmchip0/"

    def __init__(self):
        self.pins = [GPIO(12), GPIO(13), GPIO(182)]
 
        self.process = None

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

        self.pwm_channels = [0, 1, 2] #red, green, blue

    def initialize(self):
        try:
            for pin in self.pins:
                pin.setPinmux("mode1")

            for ch in self.pwm_channels:
                if not os.path.exists(self.pwm_prefix + "/pwm" + str(ch)):
                    with open(self.pwm_prefix + "export", "w") as f:
                        f.write(str(ch))

            for ch in self.pwm_channels:
                with open(self.pwm_prefix + "pwm" + str(ch) + "/enable", "w") as f:
                    f.write("1")

            for ch in self.pwm_channels:
                with open(self.pwm_prefix + "pwm" + str(ch) + "/period", "w") as f:
                    f.write("1000000")
        except IOError as error:
            print error
            return False
        
        return True


    def set_duty_cycle(self, channel, percentage=100):
        #0% = 1000000
        #100% = 0
        duty_value = int((100 - percentage) * 10000)

        try:
            with open(self.pwm_prefix + "pwm" + str(channel) + "/duty_cycle", "w") as f: 
                f.write(str(duty_value))
        except IOError as error:
            print error
            return False
        
        return True

    def set_color(self, color, power_percentage=100):
        if color in self.colors_dict.keys():
            for channel in self.pwm_channels:
                if not self.set_duty_cycle(channel, self.colors_dict[color][channel]*\
                        power_percentage):
                    return False
            return True
        else:
            return False

    def pulse_color(self, color, delay=0.5):
        number_of_steps = 100
        step = 100 / number_of_steps #100 - power_percentage
        delay = float(delay) / number_of_steps / 2

        for brightness in xrange(0, 100+step, step):
            if not self.set_color(color, brightness):
                return False
            time.sleep(delay)

        for brightness in xrange(100, -step, -step):
            if not self.set_color(color, brightness):
                return False
            time.sleep(delay)

        return True

    def start_blinker(self, pattern, delay=0.5):
        return self.__start(pattern, delay, self.blink_pattern)

    def start_pulser(self, pattern, delay=0.5):
        return self.__start(pattern, delay, self.pulse_pattern)

    def __start(self, pattern, delay, function):
    	#pattern example: "red,blue,off"
        if pattern:
    	    for color in pattern.split(","):
                if color not in self.colors_dict.keys():
                    return False
    	else:
    	    return False

        if self.process is not None:
            self.stop()

        if self.process is None:
            self.process = Process(target=function, args=(pattern, delay))
            self.process.start()
            return True

        return False

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process.join()
            self.process = None

    def blink_pattern(self, pattern, delay=0.5):
        colors =  pattern.split(",")

    	while True:
            for color in colors:
                self.set_color(color)
                time.sleep(delay)

    def pulse_pattern(self, pattern, delay=0.5):
        colors =  pattern.split(",")

        while True:
            for color in colors:
                self.pulse_color(color, delay)
                time.sleep(0.1)

