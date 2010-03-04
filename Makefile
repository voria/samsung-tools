install_dir=install -d -m 755
install_file=install -m 644
install_script=install -m 755

install: install_services install_cli install_gui
	
install_services:
	$(install_dir) $(DESTDIR)/usr/lib/samsung-tools/backends/
	$(install_file) backends/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/
	$(install_dir) $(DESTDIR)/usr/lib/samsung-tools/backends/system/util/
	$(install_file) backends/system/util/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/system/util/
	$(install_file) backends/system/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/system/
	$(install_dir) $(DESTDIR)/usr/lib/samsung-tools/backends/session/util/
	$(install_file) backends/session/util/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/session/util/
	$(install_file) backends/session/*.py $(DESTDIR)/usr/lib/samsung-tools/backends/session/
	$(install_script) *-service.py $(DESTDIR)/usr/lib/samsung-tools/
	$(install_dir) $(DESTDIR)/etc/dbus-1/system.d/
	$(install_file) bus/config/org.voria.SamsungTools.System.conf $(DESTDIR)/etc/dbus-1/system.d/
	$(install_dir) $(DESTDIR)/usr/share/dbus-1/system-services/
	$(install_file) bus/services/org.voria.SamsungTools.System.service $(DESTDIR)/usr/share/dbus-1/system-services/
	$(install_dir) $(DESTDIR)/usr/share/dbus-1/services/
	$(install_file) bus/services/org.voria.SamsungTools.Session.service $(DESTDIR)/usr/share/dbus-1/services/
	$(install_dir) $(DESTDIR)/etc/samsung-tools/
	$(install_file) configs/*.conf $(DESTDIR)/etc/samsung-tools/
	$(install_dir) $(DESTDIR)/etc/pm/sleep.d/
	$(install_script) sleep.d/20_samsung-tools $(DESTDIR)/etc/pm/sleep.d/
	$(install_dir) $(DESTDIR)/etc/init/
	$(install_file) upstart/samsung-tools.conf $(DESTDIR)/etc/init/
	
install_cli: install_services
	$(install_dir) $(DESTDIR)/usr/bin/
	$(install_script) samsung-tools.py $(DESTDIR)/usr/bin/samsung-tools

install_gui: install_cli
	$(install_dir) $(DESTDIR)/usr/lib/samsung-tools/gui/glade/
	$(install_file) gui/glade/*.glade $(DESTDIR)/usr/lib/samsung-tools/gui/glade/
	$(install_dir) $(DESTDIR)/usr/bin/
	$(install_script) samsung-tools-preferences.py $(DESTDIR)/usr/bin/samsung-tools-preferences
	$(install_dir) $(DESTDIR)/usr/share/applications/
	$(install_file) desktop/*.desktop $(DESTDIR)/usr/share/applications/

uninstall:
	rm -rf $(DESTDIR)/usr/bin/samsung-tools
	rm -rf $(DESTDIR)/usr/bin/samsung-tools-preferences
	rm -rf $(DESTDIR)/usr/lib/samsung-tools/
	rm -rf $(DESTDIR)/etc/dbus-1/system.d/org.voria.SamsungTools.System.conf
	rm -rf $(DESTDIR)/usr/share/dbus-1/system-services/org.voria.SamsungTools.System.service
	rm -rf $(DESTDIR)/usr/share/dbus-1/services/org.voria.SamsungTools.Session.service
	rm -rf $(DESTDIR)/etc/samsung-tools/
	rm -rf $(DESTDIR)/etc/pm/sleep.d/20_samsung-tools
	rm -rf $(DESTDIR)/etc/init/samsung-tools.conf
	rm -rf $(DESTDIR)/usr/share/applications/samsung-tools-preferences.desktop