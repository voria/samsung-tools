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
	def GetBluetoothInitialStatus(self, sender = None, conn = None):
		return systemconfig.getBluetoothInitialStatus()

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWebcamInitialStatus(self, sender = None, conn = None):
		return systemconfig.getWebcamInitialStatus()

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWirelessInitialStatus(self, sender = None, conn = None):
		return systemconfig.getWirelessInitialStatus()

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetCpufanInitialStatus(self, sender = None, conn = None):
		return systemconfig.getCpufanInitialStatus()

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetControlInterface(self, sender = None, conn = None):
		try:
			with open(CONTROL_INTERFACE, "r") as file:
				ci = file.readline()
		except:
			ci = "none"
		return ci

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetPHCVids(self, sender = None, conn = None):
		return systemconfig.getPHCVids()

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetBluetoothInitialStatus(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setBluetoothInitialStatus(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWebcamInitialStatus(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setWebcamInitialStatus(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWirelessInitialStatus(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setWirelessInitialStatus(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetCpufanInitialStatus(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setCpufanInitialStatus(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetPHCVids(self, value, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		return systemconfig.setPHCVids(value)
