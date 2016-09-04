import dbus

class ReachLED(object):
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
    def set_color(color):
        led = ReachLED.get_access_to_led()
        if led is not None:
            return led.set_color(color)
        return dbus.Boolean(False)

    @staticmethod
    def start_blinker(pattern, delay=0.5):
        led = ReachLED.get_access_to_led()
        if led is not None:
            return led.start_blinker(pattern, delay)
        return dbus.Boolean(False)

    @staticmethod
    def stop_blinker():
        led = ReachLED.get_access_to_led()
        if led is not None:
            led.stop_blinker()

