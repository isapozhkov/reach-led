###LED for Reach
After installation you can use LED wherever you want. All commands will be synchronized.

####Install:
  - `make install`
  - copy led.service.conf to `/etc/dbus-1/system.d/`
  - enable and start reachled.service

####Usage:
 - `set_color(color)`
 - `start_blinker(pattern, delay=0.5)`
 - `stop_blinker()`

```
from reachled import LED

LED.set_color("red")
```
