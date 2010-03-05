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

class Backlight(dbus.service.Object):
	""" Control backlight """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		# Check if easy-slow-down-manager is available for controlling backlight.
		# If not, fallback to using vbetool.
		self.method = None
		if os.path.exists(ESDM_PATH_BACKLIGHT):
			self.method = "esdm"
		else:
			# Try to load easy-slow-down-manager module
			command = COMMAND_MODPROBE + " " + ESDM_MODULE
			try:
				process = subprocess.Popen(command.split(),
										stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				process.communicate()
				if process.returncode == 0:
					self.method = "esdm"
				else:
					systemlog.write("WARNING: 'Backlight' - 'esdm' control method not available, using 'vbetool' as fallback.")
					self.method = "vbetool"
			except:
				systemlog.write("WARNING: 'Backlight' - COMMAND: '" + command + "' - Exception thrown. Using 'vbetool' as fallback.")
				self.method = "vbetool"
	
	def __save_status(self, status):
		""" Save backlight status (to be used only when self.method == "vbetool"). """
		if self.method != "vbetool":
			systemlog.write("WARNING: 'Backlight.__save_status()' - Trying to save status with self.method != \"vbetool\".")
			return
		try:
			if status == False:
				with open(LAST_DEVICE_STATUS_BACKLIGHT, "w") as file:
					file.write()
			else:
				os.remove(LAST_DEVICE_STATUS_BACKLIGHT)				
		except:
			systemlog.write("WARNING: 'Backlight.__save_status()' - Cannot save new status.")
	
	def __get_status(self):
		""" Return backlight status (to be used only when self.method == "vbetool"). """
		if self.method != "vbetool":
			systemlog.write("WARNING: 'Backlight.__get_status()' - Trying to get status with self.method != \"vbetool\".")
		if os.path.exists(LAST_DEVICE_STATUS_BACKLIGHT):
			return False
		else:
			return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if backlight is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		if self.method == "esdm":
			try:
				with open(ESDM_PATH_BACKLIGHT, 'r') as file:
					status = int(file.read(1))
					if status == 1:
						return True
					else:
						return False
			except:
				systemlog.write("ERROR: 'Backlight.IsEnabled()' - cannot read from '" + ESDM_PATH_BACKLIGHT + "'.")
				return True
		else: # self.method == "vbetool":
			return self.__get_status()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable backlight. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return True
		if self.method == "esdm":
			try:
				with open(ESDM_PATH_BACKLIGHT, 'w') as file:
					file.write('1')
				return True
			except:
				log_system.write("ERROR: 'Backlight.Enable()' - cannot write to '" + ESDM_PATH_BACKLIGHT + "'.")
				return False
		else: # self.method == "vbetool"
			command = COMMAND_VBETOOL + " dpms on"
			try:
				process = subprocess.Popen(command.split(),
										stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				process.communicate()
				if process.returncode != 0:
					systemlog.write("ERROR: 'Backlight.Enable()' - COMMAND: '" + command + "' FAILED.")
					return False
				else:
					self.__save_status(True)
					return True
			except:
				systemlog.write("ERROR: 'Backlight.Enable()' - COMMAND: '" + command + "' - Exception thrown.")
				return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable backlight. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsEnabled():
			return False
		if self.method == "esdm":
			try:
				with open(ESDM_PATH_BACKLIGHT, 'w') as file:
					file.write('0')
				return True
			except:
				systemlog.write("ERROR: 'Backlight.Disable()' - cannot write to '" + ESDM_PATH_BACKLIGHT + "'.")
				return False
		else: # self.method == "vbetool":
			command = COMMAND_VBETOOL + " dpms off"
			try:
				process = subprocess.Popen(command.split(),
										stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				process.communicate()
				if process.returncode != 0:
					systemlog.write("ERROR: 'Backlight.Disable()' - COMMAND: '" + command + "' FAILED.")
					return False
				else:
					self.__save_status(False)
					return True
			except:
				systemlog.write("ERROR: 'Backlight.Disable()' - COMMAND: '" + command + "' - Exception thrown.")
				return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle backlight. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
