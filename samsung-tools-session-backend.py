#!/usr/bin/env python
# coding=UTF-8

import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

from backends.globals import *
from backends.session.webcam import Webcam
from backends.session.notifications import Notification

mainloop = None

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.mainloop = None
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	# Initialize notification system
	notify = Notification()

	# Start session service
	session_bus = dbus.SessionBus()
	name = dbus.service.BusName(SESSION_INTERFACE_NAME, session_bus)
    
	General(session_bus, '/')
	Webcam(notify, session_bus, SESSION_OBJECT_PATH_WEBCAM)	
	
	mainloop = gobject.MainLoop()
	mainloop.run()
