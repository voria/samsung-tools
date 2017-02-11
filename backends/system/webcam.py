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


class Webcam(dbus.service.Object):
	""" Control webcam """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.available = self.__is_available()

	def __is_available(self):
		""" Check if a webcam is available. """
		""" Return 'True' if available, 'False' otherwise. """
		# TODO: Find a better way to check if webcam is available
		try:
			process = subprocess.Popen([COMMAND_DMESG], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split('\n')
			if process.returncode != 0:
				systemlog.write("ERROR: 'Webcam.__is_available()' - COMMAND: '" + COMMAND_DMESG + "' FAILED.")
				return False
			for line in output:
				if len(line.split("uvcvideo: Found")) > 1:
					return True
			return False
		except:
			systemlog.write("ERROR: 'Webcam.__is_available()' - COMMAND: '" + COMMAND_DMESG + "' - Exception thrown.")
			return False

	def __save_last_status(self, status):
		""" Save webcam last status. """
		try:
			if status:
				if os.path.exists(LAST_DEVICE_STATUS_WEBCAM):
					os.remove(LAST_DEVICE_STATUS_WEBCAM)
			else:
				file = open(LAST_DEVICE_STATUS_WEBCAM, "w")
				file.close()
		except:
			systemlog.write("WARNING: 'Webcam.__save_last_status()' - Cannot save last status.")

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def LastStatus(self, sender = None, conn = None):
		""" Return 'True' if last status is on, 'False' if off. """
		if not os.path.exists(LAST_DEVICE_STATUS_WEBCAM):
			return True
		else:
			return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def RestoreLastStatus(self, sender = None, conn = None):
		""" Restore last status for webcam """
		if self.LastStatus():
			self.Enable()
		else:
			self.Disable()

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsAvailable(self, sender = None, conn = None):
		""" Return 'True' if webcam control is available, 'False' otherwise. """
		return self.available

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsEnabled(self, sender = None, conn = None):
		""" Check if webcam is enabled. """
		""" Return 'True' if enabled, 'False' if disabled. """
		if not self.available:
			return False
		try:
			process = subprocess.Popen([COMMAND_LSMOD], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split()
			if process.returncode != 0:
				systemlog.write("ERROR: 'Webcam.IsEnabled()' - COMMAND: '" + COMMAND_LSMOD + "' FAILED.")
				return False
			if "uvcvideo" in output:
				status = True
			else:
				status = False
			self.__save_last_status(status)
			return status
		except:
			systemlog.write("ERROR: 'Webcam.IsEnabled()' - COMMAND: '" + COMMAND_LSMOD + "' - Exception thrown.")
			return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Enable(self, sender = None, conn = None):
		""" Enable webcam. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.available:
			return False
		if self.IsEnabled():
			return True
		command = COMMAND_MODPROBE + " uvcvideo"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				systemlog.write("ERROR: 'Webcam.Enable()' - COMMAND: '" + command + "' FAILED.")
				return False
			# Save webcam status
			self.__save_last_status(True)
			return True
		except:
			systemlog.write("ERROR: 'Webcam.Enable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Disable(self, sender = None, conn = None):
		""" Disable webcam. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.available:
			return False
		if not self.IsEnabled():
			return True
		command = COMMAND_MODPROBE + " -r uvcvideo"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
			if process.returncode != 0:
				systemlog.write("ERROR: 'Webcam.Disable()' - COMMAND: '" + command + "' FAILED.")
				return False
			# Save webcam status
			self.__save_last_status(False)
			return True
		except:
			systemlog.write("ERROR: 'Webcam.Disable()' - COMMAND: '" + command + "' - Exception thrown.")
			return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Toggle(self, sender = None, conn = None):
		""" Toggle webcam. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.available:
			return False
		if self.IsEnabled():
			return self.Disable()
		else:
			return self.Enable()
