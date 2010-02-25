# coding=UTF-8

import dbus.service

SESSION_INTERFACE_NAME = "org.voria.SamsungTools.Session"

class Webcam(dbus.service.Object):
	""" Control webcam """
	def __init__(self, interface, notify = None, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.webcam = interface
		self.notify = notify
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if webcam is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		enabled = self.webcam.IsEnabled()
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
	
