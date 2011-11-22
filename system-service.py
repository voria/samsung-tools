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
import subprocess

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
from backends.system.powermanagement import SysCtl
from backends.system.powermanagement import PowerManagement

mainloop = None

bluetooth = None
cpu = None
fan = None
webcam = None
wireless = None

class General(dbus.service.Object):
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		# Make sure the directory for last devices status exists
		if not os.path.exists(LAST_DEVICES_STATUS_DIRECTORY):
			os.mkdir(LAST_DEVICES_STATUS_DIRECTORY)
		# Select the interface we are going to use
		if self.__check_for_esdm_module():
			CONTROL_INTERFACE = "esdm"
		elif self.__check_for_sl_module():
			CONTROL_INTERFACE = "sl"
		else:
			systemlog.write("WARNING: 'General.__init__()' - Can't find any usable interface! Many of the functionalities will not work.")
			CONTROL_INTERFACE = None
	
	def __check_for_esdm_module(self):
		""" Check for the 'easy-slow-down-manager' interface. """
		""" Return 'True' if it can be used, 'False' otherwise. """
		if os.path.exists(ESDM_PATH_PERFORMANCE):
			# kernel module already loaded and ready to use
			return True
		try:
			command = COMMAND_MODPROBE + " " + ESDM_MODULE
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
		except:
			systemlog.write("WARNING: 'General.__check_for_esdm_module()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		if process.returncode != 0:
			return False
		else:
			return True
	
	def __check_for_sl_module(self):
		""" Check for the 'samsung-laptop' interface. """
		""" Return 'True' if it can be used, 'False' otherwise. """
		if os.path.exists(SL_PATH_PERFORMANCE):
			# kernel module already loaded and ready to use
			return True
		try:
			command = COMMAND_MODPROBE + " " + SL_MODULE
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
		except:
			systemlog.write("WARNING: 'General.__check_for_sl_module()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		if process.returncode != 0:
			return False
		else:
			return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def RestoreDevicesLastStatus(self, sender = None, conn = None):
		""" Restore last status for everything. """
		""" Return nothing. """
		bluetooth.RestoreLastStatus()
		webcam.RestoreLastStatus()
		wireless.RestoreLastStatus()
		fan.RestoreLastStatus()
		# Restore also PHC values, just in case they have been reset
		status = systemconfig.getPHCVids()
		if status != "":
			cpu.SetCurrentVids(status)
		
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetInitialDevicesStatus(self, sender = None, conn = None):
		""" Set initial status for everything. """
		""" Return nothing. """
		# Bluetooth
		status = systemconfig.getBluetoothInitialStatus()
		if status == "on":
			bluetooth.Enable()
		elif status == "off":
			bluetooth.Disable()
		else: # status == "last":
			bluetooth.RestoreLastStatus()
		# Webcam
		status = systemconfig.getWebcamInitialStatus()
		if status == "on":	
			webcam.Enable()
		elif status == "off":
			webcam.Disable()
		else: # status == "last"
			webcam.RestoreLastStatus()
		# Wireless
		status = systemconfig.getWirelessInitialStatus()
		if status == "on":
			wireless.Enable()
		elif status == "off":
			wireless.Disable()
		else: # status == "last"
			wireless.RestoreLastStatus()
		# CPU fan
		status = systemconfig.getCpufanInitialStatus()
		if status == "normal":
			fan.SetNormal()
		elif status == "silent":
			fan.SetSilent()
		elif status == "overclock":
			fan.SetOverclock()
		else: # status == "last"
			fan.RestoreLastStatus()
		# PHC
		status = systemconfig.getPHCVids()
		if status != "":
			cpu.SetCurrentVids(status)

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
	SysCtl(bus, SYSTEM_OBJECT_PATH_SYSCTL)
	PowerManagement(bus, SYSTEM_OBJECT_PATH_POWERMANAGEMENT)
	# We need these objects for restoring last statuses
	bluetooth = Bluetooth(bus, SYSTEM_OBJECT_PATH_BLUETOOTH)
	cpu = Cpu(bus, SYSTEM_OBJECT_PATH_CPU)
	fan = Fan(bus, SYSTEM_OBJECT_PATH_FAN)
	webcam = Webcam(bus, SYSTEM_OBJECT_PATH_WEBCAM)
	wireless = Wireless(bus, SYSTEM_OBJECT_PATH_WIRELESS)
	
	mainloop = gobject.MainLoop()
	mainloop.run()
	
