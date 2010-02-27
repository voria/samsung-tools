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

class Fan(dbus.service.Object):
	""" Control CPU fan """
	def __init__(self, notify = None, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.system_bus = None
		self.proxy = None
		self.interface = None
		self.notify = notify
	
	def __connect(self):
		""" Enable connection to system backend """
		self.system_bus = dbus.SystemBus()
		self.proxy = self.system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_FAN)
		self.interface = dbus.Interface(self.proxy, SYSTEM_INTERFACE_NAME)
	
	def __not_available(self, show_notify = True):
		""" If show_notify == True, inform the user that the CPU fan control is not available. """
		""" Return always 'False'. """
		if self.notify != None and show_notify:
			self.notify.setTitle(FAN_TITLE)
			self.notify.setMessage(FAN_NOT_AVAILABLE)
			self.notify.setIcon(STOP_ICON)
			self.notify.setUrgency("critical")
			self.notify.show()
		return False
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsAvailable(self, sender = None, conn = None):
		""" Check if the CPU fan control is available. """
		""" Return 'True' if available, 'False' if disabled. """
		self.__connect()
		return self.interface.IsAvailable()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Status(self, show_notify = True, sender = None, conn = None):
		""" Check current mode. """
		"""Return 0 if 'normal', 1 if 'silent', 2 if 'speed'. """
		""" Return 3 if any error. """
		if not self.IsAvailable():
			self.__not_available(show_notify)
			return 3
		self.__connect()
		status = self.interface.Status()
		if self.notify != None and show_notify:
			self.notify.setTitle(FAN_TITLE)
			self.notify.setUrgency("critical")
			if status == 0:
				self.notify.setMessage(FAN_STATUS_NORMAL)
				self.notify.setIcon(FAN_NORMAL_ICON)
			elif status == 1:
				self.notify.setMessage(FAN_STATUS_SILENT)
				self.notify.setIcon(FAN_SILENT_ICON)
			elif status == 2:
				self.notify.setMessage(FAN_STATUS_SPEED)
				self.notify.setIcon(FAN_SPEED_ICON)
			else: # status == 3
				self.notify.setMessage(FAN_NOT_AVAILABLE)
				self.notify.setIcon(STOP_ICON)
			self.notify.show()
		return status
			
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetNormal(self, show_notify = True, sender = None, conn = None):
		""" Turn to 'normal' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		self.__connect()
		result = self.interface.SetNormal()
		if self.notify != None and show_notify:
			self.notify.setTitle(FAN_TITLE)
			self.notify.setUrgency("critical")
			if result == True:
				self.notify.setMessage(FAN_SWITCH_NORMAL)
				self.notify.setIcon(FAN_NORMAL_ICON)
			else:
				self.notify.setMessage(FAN_NOT_AVAILABLE)
				self.notify.setIcon(STOP_ICON)
			self.notify.show()
		return result
		
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSilent(self, show_notify = True, sender = None, conn = None):
		""" Turn to 'silent' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		self.__connect()
		result = self.interface.SetSilent()
		if self.notify != None and show_notify:
			self.notify.setTitle(FAN_TITLE)
			self.notify.setUrgency("critical")
			if result == True:
				self.notify.setMessage(FAN_SWITCH_SILENT)
				self.notify.setIcon(FAN_SILENT_ICON)
			else:
				self.notify.setMessage(FAN_NOT_AVAILABLE)
				self.notify.setIcon(STOP_ICON)
			self.notify.show()
		return result
		
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSpeed(self, show_notify = True, sender = None, conn = None):
		""" Turn to 'speed' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		self.__connect()
		result = self.interface.SetSpeed()
		if self.notify != None and show_notify:
			self.notify.setTitle(FAN_TITLE)
			self.notify.setUrgency("critical")
			if result == True:
				self.notify.setMessage(FAN_SWITCH_SPEED)
				self.notify.setIcon(FAN_SPEED_ICON)
			else:
				self.notify.setMessage(FAN_NOT_AVAILABLE)
				self.notify.setIcon(STOP_ICON)
			self.notify.show()
		return result
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Cycle(self, show_notify = True, sender = None, conn = None):
		""" Set the next mode in a cyclic way. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		self.__connect()
		result = self.interface.Cycle()
		if self.notify != None and show_notify:
			self.notify.setTitle(FAN_TITLE)
			self.notify.setUrgency("critical")
			if result == True:
				status = self.Status(False) # Do not show notification				
				if status == 0:
					self.notify.setMessage(FAN_SWITCH_NORMAL)
					self.notify.setIcon(FAN_NORMAL_ICON)
				elif status == 1:
					self.notify.setMessage(FAN_SWITCH_SILENT)
					self.notify.setIcon(FAN_SILENT_ICON)
				elif status == 2:
					self.notify.setMessage(FAN_SWITCH_SPEED)
					self.notify.setIcon(FAN_SPEED_ICON)
				else: # status == 3
					self.notify.setMessage(FAN_NOT_AVAILABLE)
					self.notify.setIcon(STOP_ICON)
			else: # result == False
				self.notify.setMessage(FAN_NOT_AVAILABLE)
				self.notify.setIcon(STOP_ICON)
			self.notify.show()
		return result
