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

class Wireless(dbus.service.Object):
	""" Control wireless """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)	
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if wireless is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		iwconfig = subprocess.Popen(['/sbin/iwconfig', 'wlan0'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		output = iwconfig.communicate()
		stdout = output[0].split()
		stderr = output[1]
		if len(stderr) != 0:
			print "ERROR: Wireless.IsEnabled() - /sbin/iwconfig wlan0"
			return False
		for word in stdput:
			if word == "Tx-Power=off":
				return False
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return True
		iwconfig = subprocess.Popen(['/sbin/iwconfig', 'wlan0', 'txpower', 'auto'])
		iwconfig.communicate()
		if iwconfig.returncode != 0:
			print "ERROR: Wireless.Enable() - /sbin/iwconfig wlan0 txpower auto"
			return False
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsEnabled():
			return True
		iwconfig = subprocess.Popen(['/sbin/iwconfig', 'wlan0', 'txpower', 'off'])
		iwconfig.communicate()
		if iwconfig.returncode != 0:
			print "ERROR: Wireless.Disable() - /sbin/iwconfig wlan0 txpower off"
			return False
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
