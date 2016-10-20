define add_daemon
cp tools/led.service.conf /etc/dbus-1/system.d/
cp tools/led_daemon /usr/bin/
cp tools/reachled.service /etc/systemd/system/
systemctl enable reachled.service
systemctl start reachled.service
endef

define delete_daemon
systemctl stop reachled.service
systemctl disable reachled.service
rm -f /etc/dbus-1/system.d/led.service.conf
rm -f /usr/bin/led_daemon
rm -f /etc/systemd/system/reachled.service
endef

install:
	python setup.py install
	$(call add_daemon)
package:
	python setup.py sdist
clean:
	rm -rf build
	rm -rf dist
	rm -rf reachled.egg-info
deinit:
	$(call delete_daemon)