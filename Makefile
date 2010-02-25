install:
	mkdir -p $(DESTDIR)/usr/lib/samsung-tools/system-backend/
	cp system-backend/*.py $(DESTDIR)/usr/lib/samsung-tools/system-backend/
	mkdir -p $(DESTDIR)/usr/lib/samsung-tools/backend/
	cp backend/*.py $(DESTDIR)/usr/lib/samsung-tools/backend/
	mkdir -p $(DESTDIR)/etc/dbus-1/system.d/
	cp system-backend/*.conf $(DESTDIR)/etc/dbus-1/system.d/
	mkdir -p $(DESTDIR)/usr/share/dbus-1/system-services/
	cp system-backend/*.service $(DESTDIR)/usr/share/dbus-1/system-services/
	mkdir -p $(DESTDIR)/usr/share/dbus-1/services/
	cp backend/*.service $(DESTDIR)/usr/share/dbus-1/services/

uninstall:
	rm -rf $(DESTDIR)/usr/lib/samsung-tools/
	rm -rf $(DESTDIR)/etc/dbus-1/system.d/org.voria.SamsungTools.System.conf
	rm -rf $(DESTDIR)/usr/share/dbus-1/system-services/org.voria.SamsungTools.System.service
