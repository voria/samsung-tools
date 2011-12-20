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
import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

import gettext
_ = gettext.gettext
gettext.bindtextdomain("samsung-tools")
gettext.textdomain("samsung-tools")

from backends.globals import *
from backends.session.options import Options
from backends.session.backlight import Backlight
from backends.session.bluetooth import Bluetooth
from backends.session.cpu import Cpu
from backends.session.webcam import Webcam
from backends.session.wireless import Wireless
from backends.session.util.notifications import Notification

mainloop = None

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		# Check if user's directory and config file exist
		from os import mkdir
		from os.path import exists
		from shutil import copy
		if not exists(USER_DIRECTORY):
			mkdir(USER_DIRECTORY)
		if not exists(USER_CONFIG_FILE):
			try:
				copy(SESSION_CONFIG_FILE, USER_CONFIG_FILE)
			except:
				sessionlog.write("ERROR: 'General' - Cannot create user configuration file starting from global one.")
				try:
					open(USER_CONFIG_FILE, "w").close()
				except:
					sessionlog.write("ERROR: 'General' - Cannot create an empty user configuration file.")
					pass

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	# Disable session service for root user
	if os.getuid() == 0:
		import sys
		sys.exit()

	# Initialize notification system
	notify = Notification()

	# Start session service
	session_bus = dbus.SessionBus()
	name = dbus.service.BusName(SESSION_INTERFACE_NAME, session_bus)

	General(session_bus, SESSION_OBJECT_PATH_GENERAL)
	Backlight(session_bus, SESSION_OBJECT_PATH_BACKLIGHT)
	Options(session_bus, SESSION_OBJECT_PATH_OPTIONS)
	Bluetooth(notify, session_bus, SESSION_OBJECT_PATH_BLUETOOTH)
	Cpu(notify, session_bus, SESSION_OBJECT_PATH_CPU)
	Webcam(notify, session_bus, SESSION_OBJECT_PATH_WEBCAM)
	Wireless(notify, session_bus, SESSION_OBJECT_PATH_WIRELESS)

	mainloop = gobject.MainLoop()
	mainloop.run()
