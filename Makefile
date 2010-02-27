install:
	mkdir -p $(DESTDIR)/usr/lib/samsung-tools/
	cp *.py $(DESTDIR)/usr/lib/samsung-tools/
	mkdir -p $(DESTDIR)/usr/lib/samsung-tools/backends/
	cp -r backends/* $(DESTDIR)/usr/lib/samsung-tools/backends/
	mkdir -p $(DESTDIR)/etc/dbus-1/system.d/
	cp busconfig/* $(DESTDIR)/etc/dbus-1/system.d/
	mkdir -p $(DESTDIR)/usr/share/dbus-1/system-services/
	cp services/org.voria.SamsungTools.System.service $(DESTDIR)/usr/share/dbus-1/system-services/
	mkdir -p $(DESTDIR)/usr/share/dbus-1/services/
	cp services/org.voria.SamsungTools.Session.service $(DESTDIR)/usr/share/dbus-1/services/
	mkdir -p $(DESTDIR)/etc/
	cp samsung-tools.conf $(DESTDIR)/etc/

uninstall:
	rm -rf $(DESTDIR)/usr/lib/samsung-tools/
	rm -rf $(DESTDIR)/etc/dbus-1/system.d/org.voria.SamsungTools.System.conf
	rm -rf $(DESTDIR)/usr/share/dbus-1/system-services/org.voria.SamsungTools.System.service
	rm -rf $(DESTDIR)/usr/share/dbus-1/services/org.voria.SamsungTools.Session.service
	rm -rf $(DESTDIR)/etc/samsung-tools/