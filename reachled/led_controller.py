# This program is placed under the GPL license.
# Copyright (c) 2016, Emlid Limited
# All rights reserved.

# If you are interested in using this program as a part of a
# closed source project, please contact Emlid Limited (info@emlid.com).

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import dbus


class LED(object):
    @staticmethod
    def get_access_to_led():
        try:
            bus = dbus.SystemBus()
            the_object = bus.get_object("led.service", "/led/service")
            return dbus.Interface(the_object, "led.service")
        except dbus.exceptions.DBusException as error:
            print error
            return None
      
    @staticmethod
    def set_color(color, power_percentage=100):
        led = LED.get_access_to_led()
        if led is not None:
            return led.set_color(color, power_percentage)
        return dbus.Boolean(False)

    @staticmethod
    def pulse_color(color, delay=0.5):
        led = LED.get_access_to_led()
        if led is not None:
            return led.pulse_color(color, delay)
        return dbus.Boolean(False)

    @staticmethod
    def start_blinker(pattern, delay=0.5):
        led = LED.get_access_to_led()
        if led is not None:
            return led.start_blinker(pattern, delay)
        return dbus.Boolean(False)

    @staticmethod
    def start_pulser(pattern, delay=0.5):
        led = LED.get_access_to_led()
        if led is not None:
            return led.start_pulser(pattern, delay)
        return dbus.Boolean(False)

    @staticmethod
    def stop():
        led = LED.get_access_to_led()
        if led is not None:
            led.stop()

