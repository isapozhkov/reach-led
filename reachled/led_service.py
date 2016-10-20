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
import dbus.service
import dbus.mainloop.glib
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
from reach_led import ReachLED

class LEDService(dbus.service.Object):
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus_name = dbus.service.BusName("led.service", dbus.SystemBus())
        dbus.service.Object.__init__(self, self.bus_name, "/led/service")
        self.mainloop = GObject.MainLoop()
        self.led = ReachLED()

    def run(self):
        if self.led.initialize():
            self.mainloop.run()

    @dbus.service.method("led.service")
    def set_color(self, color, power_percentage=100):
        return self.led.set_color(color, power_percentage)

    @dbus.service.method("led.service")
    def pulse_color(self, color, delay=0.5):
        return self.led.pulse_color(color, delay)

    @dbus.service.method("led.service")
    def start_blinker(self, pattern, delay=0.5):
        return self.led.start_blinker(pattern, delay)

    @dbus.service.method("led.service")
    def start_pulser(self, pattern, delay=0.5):
        return self.led.start_pulser(pattern, delay)

    @dbus.service.method("led.service")
    def stop(self):
        self.led.stop()
