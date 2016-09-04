import dbus
import dbus.service
import dbus.mainloop.glib
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
from ReachLED import ReachLED

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
    def set_color(self, color):
        return self.led.set_color(color)

    @dbus.service.method("led.service")
    def start_blinker(self, pattern, delay=0.5):
        return self.led.start_blinker(pattern, delay)

    @dbus.service.method("led.service")
    def stop_blinker(self):
        self.led.stop_blinker()