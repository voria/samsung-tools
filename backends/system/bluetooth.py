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

import os
import subprocess
import dbus.service

from backends.globals import *

class Bluetooth(dbus.service.Object):
	""" Control bluetooth """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		
	def __save_last_status(self, status):
		""" Save bluetooth last status. """
		try:
			if status == True:
				if os.path.exists(LAST_DEVICE_STATUS_BLUETOOTH):
					os.remove(LAST_DEVICE_STATUS_BLUETOOTH)
			else:
				file = open(LAST_DEVICE_STATUS_BLUETOOTH, "w")
				file.close()
		except:
			systemlog.write("WARNING: 'Bluetooth.__save_last_status()' - Cannot save last status.")
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')	
	def LastStatus(self, sender = None, conn = None):
		""" Return 'True' if last status is on, 'False' if off. """
		if os.path.exists(LAST_DEVICE_STATUS_BLUETOOTH):
			return False
		else:
			return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def RestoreLastStatus(self, sender = None, conn = None):
		""" Restore last status for Bluetooth """
		if self.LastStatus() == True:
			self.Enable()
		else:
			self.Disable()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')	
	def IsAvailable(self, sender = None, conn = None):
		""" Check if bluetooth is available. """
		""" Return 'True' if available, 'False' if disabled. """
		command = COMMAND_RFKILL + " list bluetooth"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0]
			if process.returncode != 0:
				systemlog.write("ERROR: 'Bluetooth.IsAvailable()' - COMMAND: '" + command + "' FAILED.")
				return False
			if "Bluetooth" in output:
				return True
			else:
				return False
		except:
			systemlog.write("ERROR: 'Bluetooth.IsAvailable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if bluetooth is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		if not self.IsAvailable():
			return False
		command = COMMAND_RFKILL + " list bluetooth"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0]
			if process.returncode != 0:
				systemlog.write("ERROR: 'Bluetooth.IsEnabled()' - COMMAND: '" + command + "' FAILED.")
				return False
			if output.split()[5] == "yes":
				status = False
			else:
				status = True
			self.__save_last_status(status)
			return status
		except:
			systemlog.write("ERROR: 'Bluetooth.IsEnabled()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.IsEnabled():
			return True
		# Enable radio
		command = COMMAND_RFKILL + " unblock bluetooth"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				systemlog.write("ERROR: 'Bluetooth.Enable()' - COMMAND: '" + command + "' FAILED.")
				return False
		except:
			systemlog.write("ERROR: 'Bluetooth.Enable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		# Save bluetooth status
		self.__save_last_status(True)
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if not self.IsEnabled():
			return True
		# Disable radio
		command = COMMAND_RFKILL + " block bluetooth"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				systemlog.write("ERROR: 'Bluetooth.Disable()' - COMMAND: '" + command + "' FAILED.")
				return False
		except:
			systemlog.write("ERROR: 'Bluetooth.Disable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		# Save bluetooth status
		self.__save_last_status(False)
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
