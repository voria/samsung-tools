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


class Backlight(dbus.service.Object):
	""" Control backlight """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)

	def __connect(self):
		""" Enable connection to system backend """
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_BACKLIGHT)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		sessionlog.write("ERROR: 'Backlight.__connect()' - 3 attempts to connect to system bus failed.")
		return None

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if backlight is enabled. """
		""" Return 'True' if enabled, 'False' if disabled or any error. """
		interface = self.__connect()
		if not interface:
			return False
		return interface.IsEnabled()

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable backlight. """
		""" Return 'True' on success, 'False' otherwise. """
		interface = self.__connect()
		if not interface:
			return False
		return interface.Enable()

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable backlight. """
		""" Return 'True' on success, 'False' otherwise. """
		interface = self.__connect()
		if not interface:
			return False
		return interface.Disable()

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle backlight. """
		""" Return 'True' on success, 'False' otherwise. """
		interface = self.__connect()
		if not interface:
			return False
		return interface.Toggle()
