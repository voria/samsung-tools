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
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetBacklightHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for backlight control. """
		return sessionconfig.getBacklightHotkey()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetBluetoothHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for bluetooth control. """
		return sessionconfig.getBluetoothHotkey()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetFanHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for fan control. """
		return sessionconfig.getFanHotkey()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWebcamHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for webcam control. """
		return sessionconfig.getWebcamHotkey()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWirelessHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for wireless control. """
		return sessionconfig.getWirelessHotkey()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetBacklightHotkey(self, hotkey, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		# TODO: set hotkey (using xbindkeys?)
		return sessionconfig.setBacklightHotkey(hotkey)

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetBluetoothHotkey(self, hotkey, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		# TODO: set hotkey (using xbindkeys?)
		return sessionconfig.setBluetoothHotkey(hotkey)
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanHotkey(self, hotkey, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		# TODO: set hotkey (using xbindkeys?)
		return sessionconfig.setFanHotkey(hotkey)

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWebcamHotkey(self, hotkey, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		# TODO: set hotkey (using xbindkeys?)
		return sessionconfig.setWebcamHotkey(hotkey)

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWirelessHotkey(self, hotkey, sender = None, conn = None):
		""" Return 'True' on success, 'False' otherwise. """
		# TODO: set hotkey (using xbindkeys?)
		return sessionconfig.setWirelessHotkey(hotkey)
