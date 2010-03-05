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

class Fan(dbus.service.Object):
	""" Control CPU fan through easy-slow-down-manager interface """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsAvailable(self, sender = None, conn = None):
		""" Check if the CPU fan control is available. """
		""" Return 'True' if available, 'False' otherwise. """
		if os.path.exists(ESDM_PATH_FAN):
			return True
		else:
			# Try to load easy-slow-down-manager module
			command = COMMAND_MODPROBE + " " + ESDM_MODULE
			try:
				process = subprocess.Popen(command.split(),
										stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				process.communicate()
				if process.returncode != 0:
					systemlog.write("ERROR: 'Fan.IsAvailable()' - COMMAND: '" + command + "' FAILED.")
					return False
				else:
					return True
			except:
				systemlog.write("ERROR: 'Fan.IsAvailable()' - COMMAND: '" + command + "' - Exception thrown.")
				return False	
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Status(self, sender = None, conn = None):
		""" Get current mode. """
		"""Return 0 if 'normal', 1 if 'silent', 2 if 'speed'. """
		""" Return 3 if any error. """
		if not self.IsAvailable():
			return 3
		try:
			with open(ESDM_PATH_FAN, 'r') as file:
				return int(file.read(1))
		except:
			systemlog.write("ERROR: 'Fan.Status()' - cannot read from '" + ESDM_PATH_FAN + "'.")
			return 3
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetNormal(self, sender = None, conn = None):
		""" Set 'normal' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		try:
			with open(ESDM_PATH_FAN, 'w') as file:
				file.write('0')
			return True
		except:
			systemlog.write("ERROR: 'Fan.SetNormal()' - cannot write to '" + ESDM_PATH_FAN + "'.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSilent(self, sender = None, conn = None):
		""" Set 'silent' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		try:
			with open(ESDM_PATH_FAN, 'w') as file:
				file.write('1')
			return True
		except:
			systemlog.write("ERROR: 'Fan.SetSilent()' - cannot write to '" + ESDM_PATH_FAN + "'.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSpeed(self, sender = None, conn = None):
		""" Set 'speed' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		try:
			with open(ESDM_PATH_FAN, 'w') as file:
				file.write('2')
			return True
		except:
			systemlog.write("ERROR: 'Fan.SetSpeed()' - cannot write to '" + ESDM_PATH_FAN + "'.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Cycle(self, sender = None, conn = None):
		""" Set the next mode in a cyclic way. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		current = self.Status()
		if current == 0:
			return self.SetSilent()
		if current == 1:
			return self.SetSpeed()
		if current == 2:
			return self.SetNormal()
		return False
