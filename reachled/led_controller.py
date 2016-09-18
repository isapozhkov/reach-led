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

