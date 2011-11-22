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
import dbus.service

from backends.globals import *

class Fan(dbus.service.Object):
	""" Control CPU Fan """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		try:
			with open(CONTROL_INTERFACE, "r") as file:
				self.method = file.readline()
		except:
			self.method = "none"
	
	def __save_last_status(self, status):
		""" Save fan last status. """
		try:
			if status == "normal":
				if os.path.exists(LAST_DEVICE_STATUS_CPUFAN):
					os.remove(LAST_DEVICE_STATUS_CPUFAN)
			else:
				file = open(LAST_DEVICE_STATUS_CPUFAN, "w")
				file.write(status)
				file.close()
		except:
			systemlog.write("WARNING: 'Fan.__save_last_status()' - Cannot save last status.")
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsAvailable(self, sender = None, conn = None):
		""" Check if the CPU fan control is available. """
		""" Return 'True' if available, 'False' otherwise. """
		if self.method == "none":
			return False
		else:
			return True
			
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')		
	def LastStatus(self, sender = None, conn = None):
		""" Return last status for CPU fan. """
		if not os.path.exists(LAST_DEVICE_STATUS_CPUFAN):
			return "normal"
		else:
			with open(LAST_DEVICE_STATUS_CPUFAN, "r") as file:
				return file.readline()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def RestoreLastStatus(self, sender = None, conn = None):
		""" Restore last status for CPU fan. """
		laststatus = self.LastStatus()
		if laststatus == "normal":
			self.SetNormal()
		elif laststatus == "silent":
			self.SetSilent()
		else:
			self.SetOverclock()
		
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Status(self, sender = None, conn = None):
		""" Get current fan mode. """
		"""Return 0 if 'normal', 1 if 'silent', 2 if 'overclock'. """
		""" Return 3 if any error. """
		if not self.IsAvailable():
			return 3
		if self.method == "esdm":
			try:
				with open(ESDM_PATH_PERFORMANCE, 'r') as file:
					status = int(file.read(1))
					if status == 0:
						self.__save_last_status("normal")
					elif status == 1:
						self.__save_last_status("silent")
					else: # status == 2
						self.__save_last_status("overclock")
			except:
				systemlog.write("ERROR: 'Fan.Status()' - cannot read from '" + ESDM_PATH_PERFORMANCE + "'.")
				status = 3
		else: # self.method == "sl"
			try:
				with open(SL_PATH_PERFORMANCE, 'r') as file:
					s = file.read()[0:-1]
					self.__save_last_status(s)
					if s == "normal":
						status = 0
					elif s == "silent":
						status = 1
					else: # s == "overclock"
						status = 2
			except:
				systemlog.write("ERROR: 'Fan.Status()' - cannot read from '" + SL_PATH_PERFORMANCE + "'.")
				status = 3
		return status
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetNormal(self, sender = None, conn = None):
		""" Set fan to 'normal' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.method == "esdm":
			try:
				with open(ESDM_PATH_PERFORMANCE, 'w') as file:
					file.write('0')
			except:
				systemlog.write("ERROR: 'Fan.SetNormal()' - cannot write to '" + ESDM_PATH_PERFORMANCE + "'.")
				return False
		else: # self.method == "sl"
			try:
				with open(SL_PATH_PERFORMANCE, 'w') as file:
					file.write("normal")
			except:
				systemlog.write("ERROR: 'Fan.SetNormal()' - cannot write to '" + SL_PATH_PERFORMANCE + "'.")
				return False
		self.__save_last_status("normal")
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSilent(self, sender = None, conn = None):
		""" Set fan to 'silent' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.method == "esdm":
			try:
				with open(ESDM_PATH_PERFORMANCE, 'w') as file:
					file.write('1')
			except:
				systemlog.write("ERROR: 'Fan.SetSilent()' - cannot write to '" + ESDM_PATH_PERFORMANCE + "'.")
				return False
		else: # self.method == "sl"
			try:
				with open(SL_PATH_PERFORMANCE, 'w') as file:
					file.write("silent")
			except:
				systemlog.write("ERROR: 'Fan.SetSilent()' - cannot write to '" + SL_PATH_PERFORMANCE + "'.")
				return False
		self.__save_last_status("silent")
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetOverclock(self, sender = None, conn = None):
		""" Set fan to 'overclock' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.method == "esdm":
			try:
				with open(ESDM_PATH_PERFORMANCE, 'w') as file:
					file.write('2')
			except:
				systemlog.write("ERROR: 'Fan.Setoverclock()' - cannot write to '" + ESDM_PATH_PERFORMANCE + "'.")
				return False
		else: # self.method == "sl"
			try:
				with open(SL_PATH_PERFORMANCE, 'w') as file:
					file.write("overclock")
			except:
				systemlog.write("ERROR: 'Fan.SetOverclock()' - cannot write to '" + SL_PATH_PERFORMANCE + "'.")
				return False
		self.__save_last_status("overclock")
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Cycle(self, sender = None, conn = None):
		""" Set the next fan mode in a cyclic way. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		current = self.Status()
		if current == 0:
			return self.SetSilent()
		if current == 1:
			return self.SetOverclock()
		if current == 2:
			return self.SetNormal()
		return False
