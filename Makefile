install_dir=install -d -m 755
install_file=install -m 644
install_script=install -m 755

install:
	$(install_dir) $(DESTDIR)/usr/lib/samsung-tools/backends/session/util/
	$(install_file) backends/session/util/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/session/util/
	$(install_file) backends/session/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/session/
	$(install_dir) $(DESTDIR)/usr/lib/samsung-tools/backends/system/
	$(install_file) backends/system/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/system/
	$(install_script) *.py $(DESTDIR)/usr/lib/samsung-tools/
	$(install_dir) $(DESTDIR)/usr/bin/
	$(install_script) samsung-tools $(DESTDIR)/usr/bin/
	$(install_dir) $(DESTDIR)/etc/dbus-1/system.d/
	$(install_file) busconfig/* $(DESTDIR)/etc/dbus-1/system.d/
	$(install_dir) $(DESTDIR)/usr/share/dbus-1/system-services/
	$(install_file) services/org.voria.SamsungTools.System.service $(DESTDIR)/usr/share/dbus-1/system-services/
	$(install_dir) $(DESTDIR)/usr/share/dbus-1/services/
	$(install_file) services/org.voria.SamsungTools.Session.service $(DESTDIR)/usr/share/dbus-1/services/
	$(install_dir) $(DESTDIR)/etc/
	$(install_file) samsung-tools.conf $(DESTDIR)/etc/

uninstall:
	rm -rf $(DESTDIR)/usr/bin/samsung-tools
	rm -rf $(DESTDIR)/usr/lib/samsung-tools/
	rm -rf $(DESTDIR)/etc/dbus-1/system.d/org.voria.SamsungTools.System.conf
	rm -rf $(DESTDIR)/usr/share/dbus-1/system-services/org.voria.SamsungTools.System.service
	rm -rf $(DESTDIR)/usr/share/dbus-1/services/org.voria.SamsungTools.Session.service
	rm -rf $(DESTDIR)/etc/samsung-tools/