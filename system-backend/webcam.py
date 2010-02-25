# coding=UTF-8

import subprocess
import dbus.service

WEBCAM_INTERFACE_NAME = "org.voria.SamsungTools.System.Webcam"

class Webcam(dbus.service.Object):
	""" Control webcam """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
	
	@dbus.service.method(WEBCAM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if webcam is enabled by parsing the output of lsmod. """
		""" Return 'True' if enabled, 'False' if disabled. """
		lsmod = subprocess.Popen(['lsmod'], stdout = subprocess.PIPE)
		output = lsmod.communicate()[0].split()
		for word in output:
			if word == "uvcvideo":
				return True
		return False
	
	@dbus.service.method(WEBCAM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable webcam. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return True
		modprobe = subprocess.Popen(['modprobe', 'uvcvideo'])
		modprobe.communicate()
		if modprobe.returncode != 0:
			print "ERROR: Webcam.Enable() - modprobe uvcvideo"
			return False
		return True
	
	@dbus.service.method(WEBCAM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable webcam. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsEnabled():
			return True
		modprobe = subprocess.Popen(['modprobe', '-r', 'uvcvideo'])
		modprobe.communicate()
		if modprobe.returncode != 0:
			print "ERROR: Bluetooth.Disable() - modprobe -r uvcvideo"
			return False
		return True
	
	@dbus.service.method(WEBCAM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle webcam. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
