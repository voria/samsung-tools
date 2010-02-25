#!/usr/bin/env python
# coding=UTF-8

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

from backends.globals import *
from backends.system.bluetooth import Bluetooth
from backends.system.webcam import Webcam
from backends.system.wireless import Wireless

mainloop = None

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.mainloop = None
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	bus = dbus.SystemBus()
	name = dbus.service.BusName(SYSTEM_INTERFACE_NAME, bus)
    
	General(bus, SYSTEM_OBJECT_PATH_GENERAL)
	Bluetooth(bus, SYSTEM_OBJECT_PATH_BLUETOOTH)
	Webcam(bus, SYSTEM_OBJECT_PATH_WEBCAM)
	Wireless(bus, SYSTEM_OBJECT_PATH_WIRELESS)
	
	mainloop = gobject.MainLoop()
	mainloop.run()
	
