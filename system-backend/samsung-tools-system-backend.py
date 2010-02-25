#!/usr/bin/env python
# coding=UTF-8

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

from wireless import Wireless
from bluetooth import Bluetooth

mainloop = None

#class SamsungToolsSystemException(dbus.DBusException):
#	_dbus_error_name = "org.voria.SamsungToolsSystemException"

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.mainloop = None
	
	@dbus.service.method("org.voria.SamsungTools.System", in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	bus = dbus.SystemBus()
	name = dbus.service.BusName('org.voria.SamsungTools.System', bus)
    
	General(bus, '/')
	Wireless(bus, '/Wireless')
	Bluetooth(bus, '/Bluetooth')
	
	mainloop = gobject.MainLoop()
	mainloop.run()
	
