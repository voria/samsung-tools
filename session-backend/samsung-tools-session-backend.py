#!/usr/bin/env python
# coding=UTF-8

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

mainloop = None

SESSION_GENERAL_INTERFACE_NAME = "org.voria.SamsungTools.Session"

SYSTEM_INTERFACE_NAME = "org.voria.SamsungTools.System"
SYSTEM_OBJECT_PATH_GENERAL = "/"
SYSTEM_OBJECT_PATH_BLUETOOTH = "/Bluetooth"
SYSTEM_OBJECT_PATH_WEBCAM = "/Webcam"
SYSTEM_OBJECT_PATH_WIRELESS = "/Wireless"

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.mainloop = None
	
	@dbus.service.method(SESSION_GENERAL_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	# Connect to system service
	system_bus = dbus.SystemBus()
	# Get objects
	system_general = system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_GENERAL)
	system_bluetooth = system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_BLUETOOTH)
	system_webcam = system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_WEBCAM)
	system_wireless = system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_WIRELESS)

	# Start session service
	session_bus = dbus.SessionBus()
	name = dbus.service.BusName(SESSION_GENERAL_INTERFACE_NAME, session_bus)
    
	General(session_bus, '/')
	
	mainloop = gobject.MainLoop()
	mainloop.run()
