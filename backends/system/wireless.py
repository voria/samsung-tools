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

from __future__ import with_statement

import os
import subprocess
import dbus.service

from backends.globals import *

class Wireless(dbus.service.Object):
	""" Control wireless """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
			
	def __save_last_status(self, status):
		""" Save wireless last status. """
		try:
			if status == True:
				if os.path.exists(LAST_DEVICE_STATUS_WIRELESS):
					os.remove(LAST_DEVICE_STATUS_WIRELESS)
			else:
				file = open(LAST_DEVICE_STATUS_WIRELESS, "w")
				file.close()
		except:
			systemlog.write("WARNING: 'Wireless.__save_last_status()' - Cannot save last status.")
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')	
	def LastStatus(self, sender = None, conn = None):
		""" Return 'True' if last status is on, 'False' if off. """
		if not os.path.exists(LAST_DEVICE_STATUS_WIRELESS):
			return True
		else:
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def RestoreLastStatus(self, sender = None, conn = None):
		""" Restore last status for wireless """
		if self.LastStatus() == True:
			self.Enable()
		else:
			self.Disable()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')	
	def IsAvailable(self, sender = None, conn = None):
		""" Check if wireless control is available. """
		""" Return 'True' if available, 'False' if disabled. """
		if not os.path.exists(ESDM_PATH_WIRELESS):
			# Check if the 'esdm' module is correctly loaded
			command = COMMAND_MODPROBE + " " + ESDM_MODULE
			try:
				process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				process.communicate()
				if process.returncode != 0:
					systemlog.write("ERROR: 'Wireless.IsAvailable()' - COMMAND: '" + command + "' FAILED.")
					return False
				else:
					# Check again if the /proc entry exists now
					if not os.path.exists(ESDM_PATH_WIRELESS):
						systemlog.write("ERROR: 'Wireless.IsAvailable()' - '" + ESDM_PATH_WIRELESS + "' is missing.")
						return False
			except:
				systemlog.write("ERROR: 'Wireless.IsAvailable()' - COMMAND: '" + command + "' - Exception thrown.")
				return False
		# Everything's ok
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if wireless is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		if not self.IsAvailable():
			return False
		try:
			with open(ESDM_PATH_WIRELESS, 'r') as file:
				result = int(file.read(1))
				if result == 0:
					status = False
				else:
					status = True
				self.__save_last_status(status)	
				return status
		except:
			systemlog.write("ERROR: 'Wireless.IsEnabled()' - cannot read from '" + ESDM_PATH_WIRELESS + "'.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.IsEnabled():
			return True
		# Enable wireless through the 'easy slow down manager' interface
		try:
			with open(ESDM_PATH_WIRELESS, 'w') as file:
				file.write('1')
		except:
			systemlog.write("ERROR: 'Wireless.Enable()' - cannot write to '" + ESDM_PATH_WIRELESS + "'.")
			return False
		# Try to enable wireless even through the 'rfkill' command line utility
		try:
			command = COMMAND_RFKILL + " unblock wifi"
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		except:
			pass
		# Exec script
		try:
			command = SCRIPT_WIRELESS_ON
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		except:
			pass
		# Save wireless status
		self.__save_last_status(True)
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if not self.IsEnabled():
			return True
		# Try to disable wireless through the 'rfkill' command line utility
		try:
			command = COMMAND_RFKILL + " block wifi"
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			# Wait for the process to finish
			process.wait()
		except:
			pass
		# Disable wireless through the 'easy slow down manager' interface
		try:
			with open(ESDM_PATH_WIRELESS, 'w') as file:
				file.write('0')
		except:
			systemlog.write("ERROR: 'Wireless.Disable()' - cannot write to '" + ESDM_PATH_WIRELESS + "'.")
			return False
		# Exec script
		try:
			command = SCRIPT_WIRELESS_OFF
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		except:
			pass
		# Save wireless status
		self.__save_last_status(False)
		return True
			
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
