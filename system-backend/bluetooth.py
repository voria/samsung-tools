# coding=UTF-8

import subprocess
import dbus.service

SYSTEM_INTERFACE_NAME = "org.voria.SamsungTools.System"

class Bluetooth(dbus.service.Object):
	""" Control bluetooth """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if bluetooth is enabled by parsing the output of lsmod. """
		""" Return 'True' if enabled, 'False' if disabled. """
		lsmod = subprocess.Popen(['lsmod'], stdout = subprocess.PIPE)
		output = lsmod.communicate()[0].split()
		for word in output:
			if word == "btusb":
				return True
		return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return True
		modprobe = subprocess.Popen(['modprobe', 'btusb'])
		modprobe.communicate()
		if modprobe.returncode != 0:
			print "ERROR: Bluetooth.Enable() - modprobe btusb"
			return False
		service = subprocess.Popen(['service', 'bluetooth', 'start'])
		service.communicate()
		if service.returncode != 0:
			print "ERROR: Bluetooth.Enable() - service bluetooth start"
			return False
		hciconfig = subprocess.Popen(['hciconfig', 'hci0', 'up'])
		hciconfig.communicate()
		if hciconfig.returncode != 0:
			print "ERROR: Bluetooth.Enable() - hciconfig hci0 up"
			return False
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsEnabled():
			return True
		hciconfig = subprocess.Popen(['hciconfig', 'hci0', 'down'])
		hciconfig.communicate()
		if hciconfig.returncode != 0:
			print "ERROR: Bluetooth.Disable() - hciconfig hci0 down"
			return False
		service = subprocess.Popen(['service', 'bluetooth', 'stop'])
		service.communicate()
		if service.returncode != 0:
			print "ERROR: Bluetooth.Disable() - service bluetooth stop"
			return False
		modprobe = subprocess.Popen(['modprobe', '-r', 'btusb'])
		modprobe.communicate()
		if modprobe.returncode != 0:
			print "ERROR: Bluetooth.Disable() - modprobe -r btusb"
			return False
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
