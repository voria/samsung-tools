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

import dbus.service

from backends.globals import *
from backends.session.util.locales import *
from backends.session.util.icons import *

class Cpu(dbus.service.Object):
	""" Control CPU and Fan """
	def __init__(self, notify = None, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.notify = notify
	
	def __connect(self):
		""" Enable connection to system backend """
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_CPU)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		sessionlog.write("ERROR: 'Cpu.__connect()' - 3 attempts to connect to system bus failed.")
		return None
	
	def __not_available(self, show_notify = True):
		""" If show_notify == True, inform the user that the fan control is not available. """
		""" Return always 'False'. """
		if self.notify != None and show_notify:
			self.notify.setTitle(CPU_TITLE)
			self.notify.setMessage(CPU_FAN_NOT_AVAILABLE)
			self.notify.setIcon(STOP_ICON)
			self.notify.setUrgency("critical")
			self.notify.show()
		return False
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsFanAvailable(self, sender = None, conn = None):
		""" Check if the fan control is available. """
		""" Return 'True' if available, 'False' if disabled or any error. """
		interface = self.__connect()
		if not interface:
			return False
		return interface.IsFanAvailable()

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsTempAvailable(self, sender = None, conn = None):
		""" Check if temperature reading is available. """
		""" Return 'True' if available, 'False' if disabled or any error. """
		interface = self.__connect()
		if not interface:
			return False
		return interface.IsFanAvailable()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetCpuTemp(self, sender = None, conn = None):
		""" Get the current CPU temperature. """
		""" Return 'none' if temperature reading is not available. """
		interface = self.__connect()
		return interface.GetCpuTemp()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetFanMode(self, show_notify = True, sender = None, conn = None):
		""" Get current fan mode. """
		"""Return 0 if 'normal', 1 if 'silent', 2 if 'speed'. """
		""" Return 3 if any error. """
		if not self.IsFanAvailable():
			self.__not_available(show_notify)
			return 3
		interface = self.__connect()
		if not interface:
			return 3
		status = interface.GetFanMode()
		if self.notify != None and show_notify:
			self.notify.setTitle(CPU_TITLE)
			self.notify.setUrgency("critical")
			if status == 0:
				message = CPU_FAN_STATUS_NORMAL
				self.notify.setIcon(CPU_NORMAL_ICON)
			elif status == 1:
				message = CPU_FAN_STATUS_SILENT
				self.notify.setIcon(CPU_SILENT_ICON)
			elif status == 2:
				message = CPU_FAN_STATUS_SPEED
				self.notify.setIcon(CPU_SPEED_ICON)
			else: # status == 3
				self.__not_available(show_notify)
				return 3
			temp = self.GetCpuTemp()
			if temp != "none":
				message += "\n" + CPU_TEMP + " " + temp
			self.notify.setMessage(message)
			self.notify.show()
		return status
			
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanNormal(self, show_notify = True, sender = None, conn = None):
		""" Set fan to 'normal' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsFanAvailable():
			return self.__not_available(show_notify)
		interface = self.__connect()
		if not interface:
			return False
		result = interface.SetFanNormal()
		if self.notify != None and show_notify:
			self.notify.setTitle(CPU_TITLE)
			self.notify.setUrgency("critical")
			if result == True:
				message = CPU_FAN_SWITCH_NORMAL
				self.notify.setIcon(CPU_NORMAL_ICON)
			else:
				return self.__not_available(show_notify)
			temp = self.GetCpuTemp()
			if temp != "none":
				message += "\n" + CPU_TEMP + " " + temp
			self.notify.setMessage(message)
			self.notify.show()
		return result
		
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSilent(self, show_notify = True, sender = None, conn = None):
		""" Set fan to 'silent' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		interface = self.__connect()
		if not interface:
			return False
		result = interface.SetFanSilent()
		if self.notify != None and show_notify:
			self.notify.setTitle(CPU_TITLE)
			self.notify.setUrgency("critical")
			if result == True:
				message = CPU_FAN_SWITCH_SILENT
				self.notify.setIcon(CPU_SILENT_ICON)
			else:
				return self.__not_available(show_notify)
			temp = self.GetCpuTemp()
			if temp != "none":
				message += "\n" + CPU_TEMP + " " + temp
			self.notify.setMessage(message)
			self.notify.show()
		return result
		
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSpeed(self, show_notify = True, sender = None, conn = None):
		""" Set fan to 'speed' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		interface = self.__connect()
		if not interface:
			return False
		result = interface.SetFanSpeed()
		if self.notify != None and show_notify:
			self.notify.setTitle(CPU_TITLE)
			self.notify.setUrgency("critical")
			if result == True:
				message = CPU_FAN_SWITCH_SPEED
				self.notify.setIcon(CPU_SPEED_ICON)
			else:
				return self.__not_available(show_notify)
			temp = self.GetCpuTemp()
			if temp != "none":
				message += "\n" + CPU_TEMP + " " + temp
			self.notify.setMessage(message)
			self.notify.show()
		return result
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanCycle(self, show_notify = True, sender = None, conn = None):
		""" Set the next fan mode in a cyclic way. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsFanAvailable():
			return self.__not_available(show_notify)
		interface = self.__connect()
		if not interface:
			return False
		result = interface.SetFanCycle()
		if self.notify != None and show_notify:
			self.notify.setTitle(CPU_TITLE)
			self.notify.setUrgency("critical")
			if result == True:
				status = interface.GetFanMode()				
				if status == 0:
					message = CPU_FAN_SWITCH_NORMAL
					self.notify.setIcon(CPU_NORMAL_ICON)
				elif status == 1:
					message = CPU_FAN_SWITCH_SILENT
					self.notify.setIcon(CPU_SILENT_ICON)
				elif status == 2:
					message = CPU_FAN_SWITCH_SPEED
					self.notify.setIcon(CPU_SPEED_ICON)
				else: # status == 3
					return self.__not_available(show_notify)
			else: # result == False
				return self.__not_available(show_notify)
			temp = self.GetCpuTemp()
			if temp != "none":
				message += "\n" + CPU_TEMP + " " + temp
			self.notify.setMessage(message)
			self.notify.show()
		return result
