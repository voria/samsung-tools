# coding=UTF-8

import subprocess
import dbus.service

SYSTEM_WIRELESS_INTERFACE_NAME = "org.voria.SamsungTools.System.Wireless"

class Wireless(dbus.service.Object):
	""" Control wireless """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)	
	
	@dbus.service.method(SYSTEM_WIRELESS_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if wireless is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		iwconfig = subprocess.Popen(['iwconfig', 'wlan0'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		output = iwconfig.communicate()
		stdout = output[0].split()
		stderr = output[1]
		if len(stderr) != 0:
			print "ERROR: Wireless.IsEnabled() - iwconfig wlan0"
			return False
		for word in stdput:
			if word == "Tx-Power=off":
				return False
		return True
	
	@dbus.service.method(SYSTEM_WIRELESS_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return True
		iwconfig = subprocess.Popen(['iwconfig', 'wlan0', 'txpower', 'auto'])
		iwconfig.communicate()
		if iwconfig.returncode != 0:
			print "ERROR: Wireless.Enable() - iwconfig wlan0 txpower auto"
			return False
		return True
	
	@dbus.service.method(SYSTEM_WIRELESS_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsEnabled():
			return True
		iwconfig = subprocess.Popen(['iwconfig', 'wlan0', 'txpower', 'off'])
		iwconfig.communicate()
		if iwconfig.returncode != 0:
			print "ERROR: Wireless.Disable() - iwconfig wlan0 txpower off"
			return False
		return True
	
	@dbus.service.method(SYSTEM_WIRELESS_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
