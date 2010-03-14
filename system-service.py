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
import gobject

import dbus
import dbus.service
import dbus.mainloop.glib

from backends.globals import *
from backends.system.options import Options
from backends.system.backlight import Backlight
from backends.system.bluetooth import Bluetooth
from backends.system.cpu import Cpu
from backends.system.fan import Fan
from backends.system.webcam import Webcam
from backends.system.wireless import Wireless

mainloop = None

bluetooth = None
webcam = None
wireless = None

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		# Make sure the directory for last devices status exists
		if not os.path.exists(LAST_DEVICES_STATUS_DIRECTORY):
			os.mkdir(LAST_DEVICES_STATUS_DIRECTORY)	
	
	def __restore_bluetooth_status(self):
		status = bluetooth.LastStatus()
		bluetooth.Enable()
		if status == False:
			bluetooth.Disable()
	
	def __restore_webcam_status(self):
		status = webcam.LastStatus()
		webcam.Enable()
		if status == False:
			webcam.Disable()
	
	def __restore_wireless_status(self):
		status = wireless.LastStatus()
		wireless.Enable()
		if status == False:
			wireless.Disable()
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def RestoreDevicesLastStatus(self, sender = None, conn = None):
		""" Restore last status for webcam, bluetooth, wireless. """
		""" Return nothing. """
		self.__restore_bluetooth_status()
		self.__restore_webcam_status()
		self.__restore_wireless_status()
		
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetInitialDevicesStatus(self, sender = None, conn = None):
		""" Set initial status for webcam, bluetooth, wireless. """
		""" Return nothing. """
		status = systemconfig.getBluetoothInitialStatus()
		if status == "on":
			bluetooth.Enable()
		elif status == "off":
			bluetooth.Disable()
		else: # status == "last":
			self.__restore_bluetooth_status()
		status = systemconfig.getWebcamInitialStatus()
		if status == "on":	
			webcam.Enable()
		elif status == "off":
			webcam.Disable()
		else: # status == "last"
			self.__restore_webcam_status()
		status = systemconfig.getWirelessInitialStatus()
		if status == "on":
			wireless.Enable()
		elif status == "off":
			wireless.Disable()
		else: # status == "last"
			self.__restore_wireless_status()
			
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Exit(self, sender = None, conn = None):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default = True)

	bus = dbus.SystemBus()
	name = dbus.service.BusName(SYSTEM_INTERFACE_NAME, bus)
    
	General(bus, SYSTEM_OBJECT_PATH_GENERAL)
	Options(bus, SYSTEM_OBJECT_PATH_OPTIONS)
	Backlight(bus, SYSTEM_OBJECT_PATH_BACKLIGHT)
	Cpu(bus, SYSTEM_OBJECT_PATH_CPU)
	Fan(bus, SYSTEM_OBJECT_PATH_FAN)
	# We need these objects for restoring last statuses
	bluetooth = Bluetooth(bus, SYSTEM_OBJECT_PATH_BLUETOOTH)
	webcam = Webcam(bus, SYSTEM_OBJECT_PATH_WEBCAM)
	wireless = Wireless(bus, SYSTEM_OBJECT_PATH_WIRELESS)
	
	mainloop = gobject.MainLoop()
	mainloop.run()
	
