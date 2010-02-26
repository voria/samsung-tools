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
from backends.system.backlight import Backlight
from backends.system.bluetooth import Bluetooth
from backends.system.webcam import Webcam
from backends.system.wireless import Wireless

mainloop = None

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	bus = dbus.SystemBus()
	name = dbus.service.BusName(SYSTEM_INTERFACE_NAME, bus)
    
	General(bus, SYSTEM_OBJECT_PATH_GENERAL)
	Backlight(bus, SYSTEM_OBJECT_PATH_BACKLIGHT)
	Bluetooth(bus, SYSTEM_OBJECT_PATH_BLUETOOTH)
	Webcam(bus, SYSTEM_OBJECT_PATH_WEBCAM)
	Wireless(bus, SYSTEM_OBJECT_PATH_WIRELESS)
	
	mainloop = gobject.MainLoop()
	mainloop.run()
	
