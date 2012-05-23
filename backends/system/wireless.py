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

# TODO: On systems with more wireless adapters, control them individually?

class Wireless(dbus.service.Object):
	""" Control wireless """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		try:
			with open(CONTROL_INTERFACE, "r") as file:
				self.method = file.readline()
		except:
			self.method = "none"

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
		""" Return 'True' if available, 'False' if it's not. """
		command = COMMAND_RFKILL + " list wifi"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0]
			if process.returncode != 0:
				systemlog.write("ERROR: 'Wireless.IsAvailable()' - COMMAND: '" + command + "' FAILED.")
				return False
			if "Wireless" in output:
				return True
			else:
				return False
		except:
			systemlog.write("ERROR: 'Wireless.IsAvailable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if wireless is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		if not self.IsAvailable():
			return False
		if self.method == "esdm":
			try:
				with open(ESDM_PATH_WIRELESS, 'r') as file:
					status = int(file.read(1))
					if status == 0:
						result = False
					else:
						result = True
			except:
				systemlog.write("ERROR: 'Wireless.IsEnabled()' - cannot read from '" + ESDM_PATH_WIRELESS + "'.")
				return False
		else:
			command = COMMAND_RFKILL + " list wifi"
			try:
				process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				output = process.communicate()[0]
				if process.returncode != 0:
					systemlog.write("ERROR: 'Wireless.IsEnabled()' - COMMAND: '" + command + "' FAILED.")
					return False
				if "yes" in output:
					result = False
				else:
					result = True
			except:
				systemlog.write("ERROR: 'Wireless.IsEnabled()' - COMMAND: '" + command + "' - Exception thrown.")
				return False
		# Since this method is also used by Enable() and Disable(), we save here the last status
		self.__save_last_status(result)
		return result

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.method == "esdm":
			# When 'esdm' interface is enabled, enable wireless through it as the first step
			try:
				with open(ESDM_PATH_WIRELESS, 'w') as file:
					file.write('1')
			except:
				systemlog.write("ERROR: 'Wireless.Enable()' - cannot write to '" + ESDM_PATH_WIRELESS + "'.")
				return False
		# Then enable wireless through the rfkill interface
		try:
			command = COMMAND_RFKILL + " unblock wifi"
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		except:
			systemlog.write("ERROR: 'Wireless.Enable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		if not self.IsEnabled():
			# Wireless has not been enabled
			return False
		# Exec script
		try:
			command = SCRIPT_WIRELESS_ON
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		except:
			systemlog.write("WARNING: 'Wireless.Enable()' - Error while executing '" + SCRIPT_WIRELESS_ON + "'.")
			pass
		return True


	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		# Disable wireless through the rfkill interface
		try:
			command = COMMAND_RFKILL + " block wifi"
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		except:
			systemlog.write("ERROR: 'Wireless.Disable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		if self.method == "esdm":
			# If 'esdm' interface is used, disable wireless through it too
			try:
				with open(ESDM_PATH_WIRELESS, 'w') as file:
					file.write('0')
			except:
				systemlog.write("ERROR: 'Wireless.Disable()' - cannot write to '" + ESDM_PATH_WIRELESS + "'.")
				return False
		if self.IsEnabled():
			# Wireless has not been disabled
			return False
		# Exec script
		try:
			command = SCRIPT_WIRELESS_OFF
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		except:
			systemlog.write("WARNING: 'Wireless.Disable()' - Error while executing '" + SCRIPT_WIRELESS_OFF + "'.")
			pass
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
