###LED for Reach
After installation you can use ReachLED whereever you want. All commands will be synchronized.

####Install:
  - copy led.service.conf to `/etc/dbus-1/system.d/`
  - enable and start reachled.service
  - `make install`

####Usage:
 - `set_color(color)`
 - `start_blinker(pattern, delay=0.5)`
 - `stop_blinker()`

```
from reachled import ReachLED

ReachLED.set_color("red")
```
