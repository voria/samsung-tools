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
			process = subprocess.Popen(['/sbin/lsmod'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split()
			if "btusb" in output:
				return True
			else:
				return False
		except:
			log_system.write("ERROR: 'Bluetooth.__is_module_loaded()' - Exception thrown.")
			return False
	
	def __is_service_started(self):
		""" Check if bluetooth service is started. """
		""" Return 'True' if it is, 'False' otherwise. """
		try:
			process = subprocess.Popen(['/usr/sbin/service', 'bluetooth', 'status'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0]
			if process.returncode != 0:
				log_system.write("ERROR: 'Bluetooth.__is_service_started()' - COMMAND: 'service bluetooth status' FAILED.")
				return False
			if "not" in output:
				return False
			else:
				return True			
		except:
			log_system.write("ERROR: 'Bluetooth.__is_service_started()' - COMMAND: 'service bluetooth status' - Exception thrown.")
			return False
		
	def __is_radio_enabled(self):
		""" Check if bluetooth radio is enabled. """
		""" Return 'True' if it is, 'False' otherwise. """
		try:
			process = subprocess.Popen(['/usr/sbin/hciconfig', 'hci0'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split()
			if process.returncode != 0:
				log_system.write("ERROR: 'Bluetooth.__is_radio_enabled()' - COMMAND: 'hciconfig hci0' FAILED.")
				return False
			if "DOWN" in output:
				return False
			else:
				return True			
		except:
			log_system.write("ERROR: 'Bluetooth.__is_radio_enabled()' - COMMAND: 'hciconfig hci0' - Exception thrown.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')	
	def IsAvailable(self, sender = None, conn = None):
		""" Check if bluetooth is available. """
		""" Return 'True' if available, 'False' if disabled. """
		try:
			process = subprocess.Popen(['/usr/sbin/lsusb', '-v'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split()
			if "Bluetooth" in output:
				return True
			else:
				return False
		except:
			log_system.write("ERROR: 'Bluetooth.IsAvailable()' - Exception thrown.")
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if bluetooth is enabled by parsing the output of lsmod. """
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
		try:
			process = subprocess.Popen(['/sbin/modprobe', 'btusb'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				log_system.write("ERROR: 'Bluetooth.Enable()' - COMMAND: 'modprobe btusb' FAILED.")
				return False
		except:
			log_system.write("ERROR: 'Bluetooth.Enable()' - COMMAND: 'modprobe btusb' - Exception thrown.")
			return False
		try:
			process = subprocess.Popen(['/usr/sbin/service', 'bluetooth', 'start'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				log_system.write("ERROR: 'Bluetooth.Enable()' - COMMAND: 'service bluetooth start' FAILED.")
				return False
		except:
			log_system.write("ERROR: 'Bluetooth.Enable()' - COMMAND: 'service bluetooth start' - Exception thrown.")
			return False
		try:
			process = subprocess.Popen(['/usr/sbin/hciconfig', 'hci0', 'up'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				log_system.write("ERROR: 'Bluetooth.Enable()' - COMMAND: 'hciconfig hci0 up' FAILED.")
				return False
		except:
			log_system.write("ERROR: 'Bluetooth.Enable()' - COMMAND: 'hciconfig hci0 up' - Exception thrown.")
			return False
		# Set last status
		try:
			file = open(SYSTEM_DEVICE_STATUS_BLUETOOTH, "w")
			file.close()
		except:
			log_system.write("ERROR: 'Bluetooth.Enable()' - Cannot save last status.")
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
		try:
			process = subprocess.Popen(['/usr/sbin/hciconfig', 'hci0', 'down'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				log_system.write("ERROR: 'Bluetooth.Disable()' - COMMAND: 'hciconfig hci0 down' FAILED.")
				return False
		except:
			log_system.write("ERROR: 'Bluetooth.Disable()' - COMMAND: 'hciconfig hci0 down' - Exception thrown.")
			return False
		try:
			process = subprocess.Popen(['/usr/sbin/service', 'bluetooth', 'stop'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				log_system.write("ERROR: 'Bluetooth.Disable()' - COMMAND: 'service bluetooth stop' FAILED.")
				return False
		except:
			log_system.write("ERROR: 'Bluetooth.Disable()' - COMMAND: 'service bluetooth stop' - Exception thrown.")
			return False
		try:
			process = subprocess.Popen(['/sbin/modprobe', '-r', 'btusb'],
									stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				log_system.write("ERROR: 'Bluetooth.Disable()' - COMMAND: 'modprobe -r btusb' FAILED.")
				return False
		except:
			log_system.write("ERROR: 'Bluetooth.Disable()' - COMMAND: 'modprobe -r btusb' - Exception thrown.")
			return False
		# Set last status
		try:
			os.remove(SYSTEM_DEVICE_STATUS_BLUETOOTH)
		except:
			pass
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
