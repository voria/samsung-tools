install:
	mkdir -p $(DESTDIR)/usr/lib/samsung-tools/
	cp *.py $(DESTDIR)/usr/lib/samsung-tools/
	
	mkdir -p $(DESTDIR)/usr/lib/samsung-tools/backends/
	cp backends/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/
	
	mkdir -p $(DESTDIR)/usr/lib/samsung-tools/backends/session/
	cp backends/session/* $(DESTDIR)/usr/lib/samsung-tools/backends/session/
	
	mkdir -p $(DESTDIR)/usr/lib/samsung-tools/backends/system/
	cp backends/system/* $(DESTDIR)/usr/lib/samsung-tools/backends/system/
	
	mkdir -p $(DESTDIR)/etc/dbus-1/system.d/
	cp conf/* $(DESTDIR)/etc/dbus-1/system.d/
	
	mkdir -p $(DESTDIR)/usr/share/dbus-1/system-services/
	cp system-services/* $(DESTDIR)/usr/share/dbus-1/system-services/
	
	mkdir -p $(DESTDIR)/usr/share/dbus-1/services/
	cp services/* $(DESTDIR)/usr/share/dbus-1/services/

uninstall:
	rm -rf $(DESTDIR)/usr/lib/samsung-tools/
	rm -rf $(DESTDIR)/etc/dbus-1/system.d/org.voria.SamsungTools.System.conf
	rm -rf $(DESTDIR)/usr/share/dbus-1/system-services/org.voria.SamsungTools.System.service
