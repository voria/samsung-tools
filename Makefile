PREFIX?=/usr
install_dir=install -d -m 755
install_file=install -pm 644
install_script=install -pm 755

install:
	# Set work directory
	$(shell ./set_prefix.sh $(PREFIX))
	# Services
	$(install_dir) $(DESTDIR)$(PREFIX)/share/samsung-tools/backends/
	$(install_file) backends/*.py $(DESTDIR)$(PREFIX)/share/samsung-tools/backends/
	$(install_dir) $(DESTDIR)$(PREFIX)/share/samsung-tools/backends/system/util/
	$(install_file) backends/system/util/*.py $(DESTDIR)$(PREFIX)/share/samsung-tools/backends/system/util/
	$(install_file) backends/system/*.py $(DESTDIR)$(PREFIX)/share/samsung-tools/backends/system/
	$(install_dir) $(DESTDIR)$(PREFIX)/share/samsung-tools/backends/session/util/
	$(install_file) backends/session/util/*.py $(DESTDIR)$(PREFIX)/share/samsung-tools/backends/session/util/
	$(install_file) backends/session/*.py $(DESTDIR)$(PREFIX)/share/samsung-tools/backends/session/
	$(install_script) *-service.py $(DESTDIR)$(PREFIX)/share/samsung-tools/
	$(install_dir) $(DESTDIR)/etc/dbus-1/system.d/
	$(install_file) bus/config/org.voria.SamsungTools.System.conf $(DESTDIR)/etc/dbus-1/system.d/
	$(install_dir) $(DESTDIR)/usr/share/dbus-1/system-services/
	$(install_file) bus/services/org.voria.SamsungTools.System.service $(DESTDIR)/usr/share/dbus-1/system-services/
	$(install_dir) $(DESTDIR)/usr/share/dbus-1/services/
	$(install_file) bus/services/org.voria.SamsungTools.Session.service $(DESTDIR)/usr/share/dbus-1/services/
	$(install_dir) $(DESTDIR)/etc/samsung-tools/
	$(install_file) configs/*.conf $(DESTDIR)/etc/samsung-tools/
	$(install_dir) $(DESTDIR)/etc/samsung-tools/scripts/
	$(install_script) scripts/* $(DESTDIR)/etc/samsung-tools/scripts/
	$(install_dir) $(DESTDIR)/usr/lib/pm-utils/sleep.d/
	$(install_script) pm/sleep.d/20_samsung-tools $(DESTDIR)/usr/lib/pm-utils/sleep.d/
	$(install_dir) $(DESTDIR)/usr/lib/pm-utils/power.d/
	$(install_script) pm/power.d/* $(DESTDIR)/usr/lib/pm-utils/power.d/
	$(install_dir) $(DESTDIR)/usr/lib/systemd/system/
	$(install_file) systemd/samsung-tools.service $(DESTDIR)/usr/lib/systemd/system/
	# Locales
	$(shell po/install.sh $(DESTDIR))
	# CLI
	$(install_dir) $(DESTDIR)$(PREFIX)/bin/
	$(install_script) samsung-tools.py $(DESTDIR)$(PREFIX)/bin/samsung-tools
	# GUI
	$(install_dir) $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/glade/
	$(install_file) gui/glade/samsung-tools-preferences.glade $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/glade/
	$(install_file) gui/glade/samsung-tools-preferences-kernel-parameters.glade $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/glade/
	$(install_file) gui/glade/samsung-tools-preferences-power-management.glade $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/glade/
	$(install_file) gui/glade/samsung-tools-preferences-phc.glade $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/glade/
	$(install_dir) $(DESTDIR)$(PREFIX)/bin/
	$(install_script) samsung-tools-preferences.py $(DESTDIR)$(PREFIX)/bin/samsung-tools-preferences
	# Icons
	$(install_dir) $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/icons/
	$(install_file) gui/icons/samsung-tools.png $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/icons/
	$(install_file) gui/icons/fan-*.png $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/icons/
	$(install_file) gui/icons/bluetooth.png $(DESTDIR)$(PREFIX)/share/samsung-tools/gui/icons/
	# .desktop files
	$(shell desktop/prepare.sh desktop/samsung-tools-session-service.desktop.in)
	$(install_dir) $(DESTDIR)/etc/xdg/autostart/
	$(install_file) desktop/samsung-tools-session-service.desktop $(DESTDIR)/etc/xdg/autostart/
	rm -f desktop/samsung-tools-session-service.desktop
	$(shell desktop/prepare.sh desktop/samsung-tools-preferences.desktop.in)
	$(install_dir) $(DESTDIR)/usr/share/applications/
	$(install_file) desktop/samsung-tools-preferences.desktop $(DESTDIR)/usr/share/applications/
	rm -f desktop/samsung-tools-preferences.desktop

uninstall:
	$(shell po/uninstall.sh $(DESTDIR))
	rm -rf $(DESTDIR)$(PREFIX)/bin/samsung-tools
	rm -rf $(DESTDIR)$(PREFIX)/bin/samsung-tools-preferences
	rm -rf $(DESTDIR)$(PREFIX)/share/samsung-tools/
	rm -rf $(DESTDIR)/etc/dbus-1/system.d/org.voria.SamsungTools.System.conf
	rm -rf $(DESTDIR)/usr/share/dbus-1/system-services/org.voria.SamsungTools.System.service
	rm -rf $(DESTDIR)/usr/share/dbus-1/services/org.voria.SamsungTools.Session.service
	rm -rf $(DESTDIR)/etc/samsung-tools/
	rm -rf $(DESTDIR)/usr/lib/pm-utils/sleep.d/20_samsung-tools
	rm -rf $(DESTDIR)/usr/lib/pm-utils/power.d/samsung-tools_*
	rm -rf $(DESTDIR)/usr/lib/systemd/system/samsung-tools.service
	rm -rf $(DESTDIR)/etc/xdg/autostart/samsung-tools-session-service.desktop
	rm -rf $(DESTDIR)/usr/share/applications/samsung-tools-preferences.desktop

include python.mk
