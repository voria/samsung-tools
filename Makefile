install_dir=install -d -m 755
install_file=install -m 644
install_script=install -m 755

install:
	# Services
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
	# Locales
	$(shell po/install.sh ${DESTDIR})
	# CLI
	$(install_dir) $(DESTDIR)/usr/bin/
	$(install_script) samsung-tools.py $(DESTDIR)/usr/bin/samsung-tools
	# GUI
	$(install_dir) $(DESTDIR)/usr/lib/samsung-tools/gui/glade/
	$(install_file) gui/glade/samsung-tools-preferences.glade $(DESTDIR)/usr/lib/samsung-tools/gui/glade/
	$(install_dir) $(DESTDIR)/usr/bin/
	$(install_script) samsung-tools-preferences.py $(DESTDIR)/usr/bin/samsung-tools-preferences
	# Applet
	$(install_file) gui/glade/samsung-tools-applet.glade $(DESTDIR)/usr/lib/samsung-tools/gui/glade/
	$(install_script) gui/samsung-tools-applet.py $(DESTDIR)/usr/lib/samsung-tools/gui/
	# Icons
	$(install_dir) $(DESTDIR)/usr/share/icons/
	$(install_file) gui/icons/* $(DESTDIR)/usr/share/icons/
	# .desktop files
	$(shell desktop/prepare.sh desktop/samsung-tools-session-service.desktop.in)
	$(install_dir) $(DESTDIR)/etc/xdg/autostart/
	$(install_file) desktop/samsung-tools-session-service.desktop $(DESTDIR)/etc/xdg/autostart/
	rm -rf desktop/samsung-tools-session-service.desktop
	$(shell desktop/prepare.sh desktop/samsung-tools-preferences.desktop.in)
	$(install_dir) $(DESTDIR)/usr/share/applications/
	$(install_file) desktop/samsung-tools-preferences.desktop $(DESTDIR)/usr/share/applications/
	rm -rf desktop/samsung-tools-preferences.desktop
	# .server files
	$(shell bonobo/prepare.sh bonobo/samsung-tools-applet.server.in)
	$(install_dir) $(DESTDIR)/usr/lib/bonobo/servers
	$(install_file) bonobo/samsung-tools-applet.server $(DESTDIR)/usr/lib/bonobo/servers
	rm -rf bonobo/samsung-tools-applet.server

uninstall:
	$(shell po/uninstall.sh ${DESTDIR})
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
	rm -rf $(DESTDIR)/etc/xdg/autostart/samsung-tools-session-service.desktop
	rm -rf $(DESTDIR)/usr/lib/bonobo/servers/samsung-tools-applet.server
	rm -rf $(DESTDIR)/usr/share/icons/samsung-tools.*
