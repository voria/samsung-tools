#!/bin/bash
# This script is intended to be called from Makefile, it sets the correct prefix where needed

PREFIX=$1

# Update main files
sed -i "s|LOCALE_DIRECTORY = .*|LOCALE_DIRECTORY = \"$PREFIX/share/locale\"|" backends/globals.py
sed -i "s|WORK_DIRECTORY = .*|WORK_DIRECTORY = \"$PREFIX/share/samsung-tools\"|" backends/globals.py
sed -i "s|WORK_DIRECTORY = .*|WORK_DIRECTORY = \"$PREFIX/share/samsung-tools\"|" samsung-tools-preferences.py
sed -i "s|WORK_DIRECTORY = .*|WORK_DIRECTORY = \"$PREFIX/share/samsung-tools\"|" samsung-tools.py

# Update dbus services files
sed -i "s|Exec=.*|Exec=$PREFIX/share/samsung-tools/session-service.py|" bus/services/org.voria.SamsungTools.Session.service
sed -i "s|Exec=.*|Exec=$PREFIX/share/samsung-tools/system-service.py|" bus/services/org.voria.SamsungTools.System.service

# Update desktop files
sed -i "s|Icon=.*|Icon=$PREFIX/share/samsung-tools/gui/icons/samsung-tools.png|" desktop/samsung-tools-preferences.desktop.in
sed -i "s|Icon=.*|Icon=$PREFIX/share/samsung-tools/gui/icons/samsung-tools.png|" desktop/samsung-tools-session-service.desktop.in
sed -i "s|Exec=.*|Exec=$PREFIX/share/samsung-tools/session-service.py|" desktop/samsung-tools-session-service.desktop.in
