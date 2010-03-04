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

class Options(dbus.service.Object):
	""" Manage system service options """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetLastStatusRestore(self, sender = None, conn = None):
		return systemconfig.getLastStatusRestore()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWirelessToggleMethod(self, sender = None, conn = None):
		return systemconfig.getWirelessToggleMethod()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWirelessDevice(self, sender = None, conn = None):
		return systemconfig.getWirelessDevice()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWirelessModule(self, sender = None, conn = None):
		return systemconfig.getWirelessModule()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetLastStatusRestore(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setLastStatusRestore(value)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWirelessToggleMethod(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setWirelessToggleMethod(value)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWirelessDevice(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setWirelessDevice(value)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWirelessModule(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setWirelessModule(value)
