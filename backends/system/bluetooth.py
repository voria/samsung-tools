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
import subprocess
import dbus.service

from backends.globals import *

class Bluetooth(dbus.service.Object):
	""" Control bluetooth """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
	
	def __is_module_loaded(self):
		""" Check if bluetooth kernel module is loaded. """
		""" Return 'True' if it's loaded, 'False' otherwise. """
		try:
			process = subprocess.Popen([COMMAND_LSMOD],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split()
			if "btusb" in output:
				return True
			else:
				return False
		except:
			systemlog.write("ERROR: 'Bluetooth.__is_module_loaded()' - Exception thrown.")
			return False
	
	def __is_service_started(self):
		""" Check if bluetooth service is started. """
		""" Return 'True' if it is, 'False' otherwise. """
		try:
			process = subprocess.Popen([COMMAND_SERVICE, 'bluetooth', 'status'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0]
			if process.returncode != 0:
				command = COMMAND_SERVICE + " bluetooth status"
				systemlog.write("ERROR: 'Bluetooth.__is_service_started()' - COMMAND: '" + command + "' FAILED.")
				return False
			if "not" in output:
				return False
			else:
				return True			
		except:
			command = COMMAND_SERVICE + " bluetooth status"
			systemlog.write("ERROR: 'Bluetooth.__is_service_started()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		
	def __is_radio_enabled(self):
		""" Check if bluetooth radio is enabled. """
		""" Return 'True' if it is, 'False' otherwise. """
		try:
			process = subprocess.Popen([COMMAND_HCICONFIG, 'hci0'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split()
			if process.returncode != 0:
				command = COMMAND_HCICONFIG + " hci0"
				systemlog.write("ERROR: 'Bluetooth.__is_radio_enabled()' - COMMAND: '" + command + "' FAILED.")
				return False
			if "DOWN" in output:
				return False
			else:
				return True			
		except:
			command = COMMAND_HCICONFIG + " hci0"
			systemlog.write("ERROR: 'Bluetooth.__is_radio_enabled()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
	
	def __save_last_status(self, status):
		""" Save bluetooth last status. """
		try:
			if status == True:
				if os.path.exists(LAST_DEVICE_STATUS_BLUETOOTH):
					os.remove(LAST_DEVICE_STATUS_BLUETOOTH)
			else:
				file = open(LAST_DEVICE_STATUS_BLUETOOTH, "w")
				file.close()
		except:
			systemlog.write("WARNING: 'Bluetooth.__save_last_status()' - Cannot save last status.")
		
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')	
	def IsAvailable(self, sender = None, conn = None):
		""" Check if bluetooth is available. """
		""" Return 'True' if available, 'False' if disabled. """
		# FIXME: Find a better way to check if bluetooth is available
		try:
			process = subprocess.Popen([COMMAND_LSUSB, '-v'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split()
			if process.returncode != 0:
				command = COMMAND_LSUSB + " -v"
				systemlog.write("ERROR: 'Bluetooth.IsAvailable()' - COMMAND: '" + command + "' FAILED.")
				return False
			if "Bluetooth" in output:
				return True
			else:
				return False
		except:
			systemlog.write("ERROR: 'Bluetooth.IsAvailable()' - Exception thrown.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if bluetooth is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		if not self.IsAvailable():
			return False
		if self.__is_module_loaded() and self.__is_service_started() and self.__is_radio_enabled():
			return True
		else:
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.IsEnabled():
			return True
		# Load kernel module
		try:
			process = subprocess.Popen([COMMAND_MODPROBE, 'btusb'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				command = COMMAND_MODPROBE + " btusb"
				systemlog.write("ERROR: 'Bluetooth.Enable()' - COMMAND: '" + command + "' FAILED.")
				return False
		except:
			command = COMMAND_MODPROBE + " btusb"
			systemlog.write("ERROR: 'Bluetooth.Enable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		# Start bluetooth service
		try:
			process = subprocess.Popen([COMMAND_SERVICE, 'bluetooth', 'start'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				command = COMMAND_SERVICE + " bluetooth start"
				systemlog.write("ERROR: 'Bluetooth.Enable()' - COMMAND: '" + command + "' FAILED.")
				return False
		except:
			command = COMMAND_SERVICE + " bluetooth start"
			systemlog.write("ERROR: 'Bluetooth.Enable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		# Enable bluetooth radio
		try:
			process = subprocess.Popen([COMMAND_HCICONFIG, 'hci0', 'up'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				command = COMMAND_HCICONFIG + " hci0 up"
				systemlog.write("ERROR: 'Bluetooth.Enable()' - COMMAND: '" + command + "' FAILED.")
				return False
		except:
			command = COMMAND_HCICONFIG + " hci0 up"
			systemlog.write("ERROR: 'Bluetooth.Enable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		# Save bluetooth status
		self.__save_last_status(True)
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if not self.IsEnabled():
			return True
		# Disable bluetooth radio
		try:
			process = subprocess.Popen([COMMAND_HCICONFIG, 'hci0', 'down'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				command = COMMAND_HCICONFIG + " hci0 down"
				systemlog.write("ERROR: 'Bluetooth.Disable()' - COMMAND: '" + command + "' FAILED.")
				return False
		except:
			command = COMMAND_HCICONFIG + " hci0 down"
			systemlog.write("ERROR: 'Bluetooth.Disable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		# Stop bluetooth service
		try:
			process = subprocess.Popen([COMMAND_SERVICE, 'bluetooth', 'stop'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				command = COMMAND_SERVICE + " bluetooth stop"
				systemlog.write("ERROR: 'Bluetooth.Disable()' - COMMAND: '" + command + "' FAILED.")
				return False
		except:
			command = COMMAND_SERVICE + " bluetooth stop"
			systemlog.write("ERROR: 'Bluetooth.Disable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		# Remove kernel module
		try:
			process = subprocess.Popen([COMMAND_MODPROBE, '-r', 'btusb'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				command = COMMAND_MODPROBE + " -r btusb"
				systemlog.write("ERROR: 'Bluetooth.Disable()' - COMMAND: '" + command + "' FAILED.")
				return False
		except:
			command = COMMAND_MODPROBE + " -r btusb"
			systemlog.write("ERROR: 'Bluetooth.Disable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False
		# Save bluetooth status
		self.__save_last_status(False)
		return True
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle bluetooth. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return False
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
