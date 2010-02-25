#!/usr/bin/env python
# coding=UTF-8
#
# Samsung-Tools
# 
# Part of the 'Linux On My Samsung' project - <http://www.voria.org/forum>
#
# Copyleft (C) 2010 by
# Fortunato Ventre (voRia) - <vorione@gmail.com> - <http://www.voria.org>
#
# 'Samsung-Tools' is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# <http://www.gnu.org/licenses/gpl.txt>

import subprocess
import dbus.service

from backends.globals import *

class Bluetooth(dbus.service.Object):
	""" Control bluetooth """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if bluetooth is enabled by parsing the output of lsmod. """
		""" Return 'True' if enabled, 'False' if disabled. """
		lsmod = subprocess.Popen(['/sbin/lsmod'], stdout = subprocess.PIPE)
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
		modprobe = subprocess.Popen(['/sbin/modprobe', 'btusb'])
		modprobe.communicate()
		if modprobe.returncode != 0:
			print "ERROR: Bluetooth.Enable() - /sbin/modprobe btusb"
			return False
		service = subprocess.Popen(['/usr/sbin/service', 'bluetooth', 'start'])
		service.communicate()
		if service.returncode != 0:
			print "ERROR: Bluetooth.Enable() - /usr/sbin/service bluetooth start"
			return False
		hciconfig = subprocess.Popen(['/usr/sbin/hciconfig', 'hci0', 'up'])
		hciconfig.communicate()
		if hciconfig.returncode != 0:
			print "ERROR: Bluetooth.Enable() - /usr/sbin/hciconfig hci0 up"
			return False
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsEnabled():
			return True
		hciconfig = subprocess.Popen(['/usr/sbin/hciconfig', 'hci0', 'down'])
		hciconfig.communicate()
		if hciconfig.returncode != 0:
			print "ERROR: Bluetooth.Disable() - /usr/sbin/hciconfig hci0 down"
			return False
		service = subprocess.Popen(['/usr/sbin/service', 'bluetooth', 'stop'])
		service.communicate()
		if service.returncode != 0:
			print "ERROR: Bluetooth.Disable() - /usr/sbin/service bluetooth stop"
			return False
		modprobe = subprocess.Popen(['/sbin/modprobe', '-r', 'btusb'])
		modprobe.communicate()
		if modprobe.returncode != 0:
			print "ERROR: Bluetooth.Disable() - /sbin/modprobe -r btusb"
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
