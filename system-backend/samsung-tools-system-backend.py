#!/usr/bin/env python
# coding=UTF-8

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

from bluetooth import Bluetooth
from webcam import Webcam
from wireless import Wireless

mainloop = None

SYSTEM_GENERAL_INTERFACE_NAME = "org.voria.SamsungTools.System"

#class SamsungToolsSystemException(dbus.DBusException):
#	_dbus_error_name = "org.voria.SamsungToolsSystemException"

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.mainloop = None
	
	@dbus.service.method(SYSTEM_GENERAL_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	bus = dbus.SystemBus()
	name = dbus.service.BusName(SYSTEM_GENERAL_INTERFACE_NAME, bus)
    
	General(bus, '/')
	Bluetooth(bus, '/Bluetooth')
	Webcam(bus, '/Webcam')
	Wireless(bus, '/Wireless')
	
	mainloop = gobject.MainLoop()
	mainloop.run()
	
