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

VBETOOL_TEMP_FILE = "/tmp/samsung-tools-backlight-status"

class Backlight(dbus.service.Object):
	""" Control backlight """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		# Check if easy-slow-down-manager is available for controlling backlight.
		# If not, fallback to using vbetool.
		self.method = None
		if os.path.exists('/proc/easy_backlight'):
			self.method = "esdm"
		else:
			# Try to load easy-slow-down-manager module
			process = subprocess.Popen(['/sbin/modprobe', 'easy_slow_down_manager'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode == 0:
				self.method = "esdm"
			else:
				log_system.write("WARNING: 'Backlight()' - 'esdm' control method not available, using 'vbetool' as fallback.")
				self.method = "vbetool"
	
	def __save_status(self, status):
		""" Save backlight status in VBETOOL_TEMP_FILE. """
		try:
			with open(VBETOOL_TEMP_FILE, "w") as file:
				file.write(str(status))
		except:
			pass
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if backlight is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		if self.method == "esdm":
			try:
				with open('/proc/easy_backlight', 'r') as file:
					status = int(file.read(1))
					if status == 1:
						return True
					else:
						return False
			except:
				log_system.write("ERROR: 'Backlight.IsEnabled()' - cannot read from '/proc/easy_slow_down_manager'.")
				return True
		if self.method == "vbetool":
			if not os.path.exists(VBETOOL_TEMP_FILE):
				return True
			try:
				with open(VBETOOL_TEMP_FILE, 'r') as file:
					status = int(file.read(1))
					if status == 1:
						return True
					else:
						return False
			except:
				log_system.write("ERROR: 'Backlight.IsEnabled()' - cannot read from '" + VBETOOL_TEMP_FILE + "'.")
				return True
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable backlight. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.method == "esdm":
			try:
				with open('/proc/easy_backlight', 'w') as file:
					file.write('1')
				return True
			except:
				log_system.write("ERROR: 'Backlight.Enable()' - cannot write to '/proc/easy_backlight'.")
				return False
		if self.method == "vbetool":
			process = subprocess.Popen(['/usr/sbin/vbetool', 'dpms', 'on'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				log_system.write("ERROR: 'Backlight.Enable()' - COMMAND: 'vbetool dpms on'.")
				return False
			else:
				self.__save_status(1)
				return True
		return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable backlight. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.method == "esdm":
			try:
				with open('/proc/easy_backlight', 'w') as file:
					file.write('0')
				return True
			except:
				log_system.write("ERROR: 'Backlight.Disable()' - cannot write to '/proc/easy_backlight'.")
				return False
		if self.method == "vbetool":
			process = subprocess.Popen(['/usr/sbin/vbetool', 'dpms', 'off'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				log_system.write("ERROR: 'Backlight.Disable()' - COMMAND: 'vbetool dpms off'.")
				return False
			else:
				self.__save_status(0)
				return True
		return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle webcam. """
		""" Return 'True' on success, 'False' otherwise. """
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
