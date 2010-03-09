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

class Cpu(dbus.service.Object):
	""" Show CPU temperature and control CPU Fan through easy-slow-down-manager interface """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.fan_available = self.__is_fan_available()
		self.temp_available = self.__is_temp_available()
		
	def __is_fan_available(self):
		""" Check if the fan control is available. """
		""" Return 'True' if available, 'False' otherwise. """
		if os.path.exists(ESDM_PATH_CPU):
			return True
		else:
			# Try to load easy-slow-down-manager module
			command = COMMAND_MODPROBE + " " + ESDM_MODULE
			try:
				process = subprocess.Popen(command.split(),
										stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				process.communicate()
				if process.returncode != 0:
					systemlog.write("ERROR: 'Cpu.__is_fan_available()' - COMMAND: '" + command + "' FAILED.")
					return False
				else:
					return True
			except:
				systemlog.write("ERROR: 'Cpu.__is_fan_available()' - COMMAND: '" + command + "' - Exception thrown.")
				return False
	
	def __is_temp_available(self):
		""" Check if the temperature reading is available. """
		""" Return 'True' if available, 'False' otherwise. """
		if os.path.exists(CPU_TEMPERATURE_PATH):
			return True
		else:
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsFanAvailable(self, sender = None, conn = None):
		""" Return 'True' if fan control is available, 'False' otherwise. """
		return self.fan_available
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsTempAvailable(self, sender = None, conn = None):
		""" Return 'True' if temperature reading is available, 'False' otherwise. """
		return self.temp_available
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetCpuTemp(self, sender = None, conn = None):
		""" Return current CPU temperature. """
		""" Return 'none' if any error. """
		if not self.temp_available:
			return "none"
		try:
			file = open(CPU_TEMPERATURE_PATH, "r")
		except:
			systemlog.write("ERROR: 'Cpu.GetCpuTemp()' - Cannot read temperature from '" + CPU_TEMPERATURE_PATH + "'.")
			return "none"
		return file.read().split(':')[1].strip()	
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetFanMode(self, sender = None, conn = None):
		""" Get current fan mode. """
		"""Return 0 if 'normal', 1 if 'silent', 2 if 'speed'. """
		""" Return 3 if any error. """
		if not self.fan_available:
			return 3
		try:
			with open(ESDM_PATH_CPU, 'r') as file:
				return int(file.read(1))
		except:
			systemlog.write("ERROR: 'Cpu.GetFanMode()' - cannot read from '" + ESDM_PATH_CPU + "'.")
			return 3
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanNormal(self, sender = None, conn = None):
		""" Set fan to 'normal' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.fan_available:
			return False
		try:
			with open(ESDM_PATH_CPU, 'w') as file:
				file.write('0')
			return True
		except:
			systemlog.write("ERROR: 'Cpu.SetFanNormal()' - cannot write to '" + ESDM_PATH_CPU + "'.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanSilent(self, sender = None, conn = None):
		""" Set fan to 'silent' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.fan_available:
			return False
		try:
			with open(ESDM_PATH_CPU, 'w') as file:
				file.write('1')
			return True
		except:
			systemlog.write("ERROR: 'Cpu.SetFanSilent()' - cannot write to '" + ESDM_PATH_CPU + "'.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanSpeed(self, sender = None, conn = None):
		""" Set fan to 'speed' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.fan_available:
			return False
		try:
			with open(ESDM_PATH_CPU, 'w') as file:
				file.write('2')
			return True
		except:
			systemlog.write("ERROR: 'Cpu.SetFanSpeed()' - cannot write to '" + ESDM_PATH_CPU + "'.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanCycle(self, sender = None, conn = None):
		""" Set the next fan mode in a cyclic way. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.fan_available:
			return False
		current = self.GetFanMode()
		if current == 0:
			return self.SetFanSilent()
		if current == 1:
			return self.SetFanSpeed()
		if current == 2:
			return self.SetFanNormal()
		return False
