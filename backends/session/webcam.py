# coding=UTF-8

import dbus.service

from backends.globals import *

class Webcam(dbus.service.Object):
	""" Control webcam """
	def __init__(self, notify = None, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.system_bus = None
		self.proxy = None
		self.interface = None
		self.notify = notify
	
	def __connect(self):
		self.system_bus = dbus.SystemBus()
		self.proxy = self.system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_WEBCAM)
		self.interface = dbus.Interface(self.proxy, SYSTEM_INTERFACE_NAME)
		
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if webcam is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		self.__connect()
		enabled = self.interface.IsEnabled()
		if self.notify != None:
			self.notify.setTitle("Webcam")
			self.notify.setIcon("info")
			self.notify.setUrgency("normal")
			if enabled:
				self.notify.setMessage("Webcam is enabled")
			else:
				self.notify.setMessage("Webcam is disabled")
			self.notify.show()
		return enabled
	
