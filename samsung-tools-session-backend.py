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

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

from backends.globals import *
from backends.session.backlight import Backlight
from backends.session.bluetooth import Bluetooth
from backends.session.fan import Fan
from backends.session.webcam import Webcam
from backends.session.wireless import Wireless
from backends.session.util.notifications import Notification

mainloop = None

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.mainloop = None
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		# Exit the system service too, while developing.
		# TODO: remember to remove this code.
		try:
			system_bus = dbus.SystemBus()
			proxy = system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_GENERAL)
			interface = dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			interface.Exit()
		except:
			pass
		#		
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	# Initialize notification system
	notify = Notification()

	# Start session service
	session_bus = dbus.SessionBus()
	name = dbus.service.BusName(SESSION_INTERFACE_NAME, session_bus)
    
	General(session_bus, '/')
	Backlight(session_bus, SESSION_OBJECT_PATH_BACKLIGHT)
	Bluetooth(notify, session_bus, SESSION_OBJECT_PATH_BLUETOOTH)
	Fan(notify, session_bus, SESSION_OBJECT_PATH_FAN)
	Webcam(notify, session_bus, SESSION_OBJECT_PATH_WEBCAM)
	Wireless(notify, session_bus, SESSION_OBJECT_PATH_WIRELESS)
	
	
	mainloop = gobject.MainLoop()
	mainloop.run()
