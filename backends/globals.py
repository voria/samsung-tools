#!/usr/bin/env python
# coding=UTF-8
#
# Samsung-Tools
# 
# Part of the 'Linux On My Samsung' project - <http://www.voria.org/forum>
#
# Copyleft (C) 2010 by
# Fortunato Ventre (voRia) - <vorione@gmail.com> - <http://www.voria.org>
#
# 'Samsung-Tools' is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# <http://www.gnu.org/licenses/gpl.txt>

import os

from backends.log import Log

SYSTEM_CONFIG_FILE = "/etc/samsung-tools/system.conf"
SYSTEM_LOG_FILE = "/var/log/samsung-tools.log"

SESSION_CONFIG_FILE = "/etc/samsung-tools/session.conf"
try: # system service fails when trying to join $HOME, anyway this is needed only by session service
	USER_DIRECTORY = os.path.join(os.getenv('HOME'), ".samsung-tools")
	USER_CONFIG_FILE = os.path.join(USER_DIRECTORY, os.path.basename(SESSION_CONFIG_FILE))
except:
	pass

log_system = Log(SYSTEM_LOG_FILE)

SESSION_INTERFACE_NAME = "org.voria.SamsungTools.Session"
SESSION_OBJECT_PATH_GENERAL = "/"
SESSION_OBJECT_PATH_HOTKEYS = "/Hotkeys"
SESSION_OBJECT_PATH_BACKLIGHT = "/Device/Backlight"
SESSION_OBJECT_PATH_BLUETOOTH = "/Device/Bluetooth"
SESSION_OBJECT_PATH_FAN = "/Device/Fan"
SESSION_OBJECT_PATH_WEBCAM = "/Device/Webcam"
SESSION_OBJECT_PATH_WIRELESS = "/Device/Wireless"

SYSTEM_INTERFACE_NAME = "org.voria.SamsungTools.System"
SYSTEM_OBJECT_PATH_GENERAL = "/"
SYSTEM_OBJECT_PATH_BACKLIGHT = "/Device/Backlight"
SYSTEM_OBJECT_PATH_BLUETOOTH = "/Device/Bluetooth"
SYSTEM_OBJECT_PATH_FAN = "/Device/Fan"
SYSTEM_OBJECT_PATH_WEBCAM = "/Device/Webcam"
SYSTEM_OBJECT_PATH_WIRELESS = "/Device/Wireless"
