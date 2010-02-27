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

class Wireless(dbus.service.Object):
	""" Control wireless """
	def __init__(self, notify = None, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.system_bus = None
		self.proxy = None
		self.interface = None
		self.notify = notify
	
	def __connect(self):
		""" Enable connection to system backend """
		self.system_bus = dbus.SystemBus()
		self.proxy = self.system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_WIRELESS)
		self.interface = dbus.Interface(self.proxy, SYSTEM_INTERFACE_NAME)
	
	def __not_available(self, show_notify = True):
		""" If show_notify == True, inform the user that wireless is not available. """
		""" Return always 'False'. """
		if self.notify != None and show_notify:
			self.notify.setTitle(WIRELESS_TITLE)
			self.notify.setMessage(WIRELESS_NOT_AVAILABLE)
			self.notify.setIcon(STOP_ICON)
			self.notify.setUrgency("critical")
			self.notify.show()
		return False
		
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsAvailable(self, sender = None, conn = None):
		""" Check if wireless is available. """
		""" Return 'True' if available, 'False' if disabled. """
		self.__connect()
		return self.interface.IsAvailable()
			
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, show_notify = True, sender = None, conn = None):
		""" Check if wireless is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		self.__connect()
		enabled = self.interface.IsEnabled()
		if self.notify != None and show_notify:
			self.notify.setTitle(WIRELESS_TITLE)
			self.notify.setUrgency("critical")
			if enabled:
				self.notify.setIcon(WIRELESS_ENABLED_ICON)
				self.notify.setMessage(WIRELESS_STATUS_ENABLED)
			else:
				self.notify.setIcon(WIRELESS_DISABLED_ICON)
				self.notify.setMessage(WIRELESS_STATUS_DISABLED)
			self.notify.show()
		return enabled
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, show_notify = True, sender = None, conn = None):
		""" Enable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		self.__connect()
		result = self.interface.Enable()
		if self.notify != None and show_notify:
			self.notify.setTitle(WIRELESS_TITLE)
			self.notify.setUrgency("critical")
			if result == 1:
				self.notify.setIcon(WIRELESS_ENABLED_ICON)
				self.notify.setMessage(WIRELESS_ENABLED)
			else:
				self.notify.setIcon(WIRELESS_DISABLED_ICON)
				self.notify.setMessage(WIRELESS_ENABLING_ERROR)
			self.notify.show()
		return result
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, show_notify = True, sender = None, conn = None):
		""" Disable wireless. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		self.__connect()
		result = self.interface.Disable()
		if self.notify != None and show_notify:
			self.notify.setTitle(WIRELESS_TITLE)
			self.notify.setIcon(WIRELESS_DISABLED_ICON)
			self.notify.setUrgency("critical")
			if result == 1:
				self.notify.setMessage(WIRELESS_DISABLED)
			else:
				self.notify.setMessage(WIRELESS_DISABLING_ERROR)
			self.notify.show()
		return result

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, show_notify = True, sender = None, conn = None):
		""" Toggle bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available(show_notify)
		enabled = self.IsEnabled(False) # Do not show notification
		if enabled:
			return self.Disable(show_notify)
		else:
			return self.Enable(show_notify)
