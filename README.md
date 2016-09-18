###LED for Reach
After installation you can use LED wherever you want. All commands will be synchronized.

####Install:
  - `make install`
  - copy `app/led.service.conf` to `/etc/dbus-1/system.d/`
  - enable and start `app/reachled.service`

####Usage:
 - `set_color(color, power=100)`
 - `pulse_color(color, delay=0.5)`
 - `start_blinker(pattern, delay=0.5)`
 - `start_pulser(pattern, delay=0.5)`
 - `stop()`

```
from reachled import LED

LED.set_color("red")
```
