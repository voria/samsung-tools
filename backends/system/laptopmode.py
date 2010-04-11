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

import os, shutil
import dbus.service

from backends.globals import *

# laptop-mode configuration files
MAIN_CONFIG_FILE = "/etc/laptop-mode/laptop-mode.conf"
ETHERNET_CONFIG_FILE = "/etc/laptop-mode/conf.d/ethernet.conf"
HALPOLLING_CONFIG_FILE = "/etc/laptop-mode/conf.d/hal-polling.conf"
CONFIGURATIONFILESCONTROL_CONFIG_FILE = "/etc/laptop-mode/conf.d/configuration-file-control.conf"
INTELHDAPOWERSAVE_CONFIG_FILE = "/etc/laptop-mode/conf.d/intel-hda-powersave.conf"
INTELSATAPOWERMGMT_CONFIG_FILE = "/etc/laptop-mode/conf.d/intel-sata-powermgmt.conf"
SCHEDMCPOWERSAVINGS_CONFIG_FILE = "/etc/laptop-mode/conf.d/sched-mc-power-savings.conf"
USBAUTOSUSPEND_CONFIG_FILE = "/etc/laptop-mode/conf.d/usb-autosuspend.conf"
VIDEOOUT_CONFIG_FILE = "/etc/laptop-mode/conf.d/video-out.conf"

class LaptopMode(dbus.service.Object):
	""" Manage laptop-mode """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		# Check if laptop-mode is available
		self.available = False
		self.IsAvailable()

	def __write(self, file, option, value):
		""" Write the 'option=value' in the 'file' configfile. """
		""" If 'option' is not found in the config file, add it. """
		""" Return "True" on success, "False" otherwise. """
		if not self.available:
			return False
		
		optionfound = False
		try:
			oldfile = open(file, "r")
		except:
			systemlog.write("ERROR: 'LaptopMode.__write()' - '" + file + "' not found.")
			return False
		try:
			newfile = open(file + ".new", "w")
		except:
			systemlog.write("ERROR: 'LaptopMode.__write()' - cannot write the new config file.")
			oldfile.close()
			return False
		for line in oldfile:
			if line[0:1] == "#" or line == "\n":
				newfile.write(line)
			else:
				currentoption = line.split('=')[0].strip()
				if currentoption != option: # not the option we are searching for
					newfile.write(line)
				else:
					optionfound = True
					try:					
						newfile.write(option + "=" + value + "\n")
					except:
						systemlog.write("ERROR: 'LaptopMode.__write()' - cannot write the new value for '" + option + "' in the new config file.")
						oldfile.close()
						newfile.close()
						os.remove(file + ".new")
						return False
		oldfile.close()
		if optionfound == False: # option not found in current config file, add it
			newfile.write(option + "=" + value + "\n")
		newfile.close()
		try:
			os.remove(file)
		except:
			systemlog.write("ERROR: 'LaptopMode.__write()' - cannot replace old '" + file + "' with the new version.")
			os.remove(file + ".new")
			return False
		shutil.move(file + ".new", file)
		return True
	
	def __read(self, file, option):
		""" Read the 'option' value in the 'file' configfile. """
		""" Return the read value, or 'None' if any error. """
		if not self.available:
			return None
		try:
			f = open(file, "r")
		except:
			systemlog.write("ERROR: 'LaptopMode.__read()' - '" + file + "' not found.")
			return None
		for line in f:
			if line[0:1] != "#" and line != "\n":
				currentoption = line.split('=')[0].strip()
				if currentoption == option:
					f.close()
					return line.split('=')[1].strip()
		# Option not found
		f.close()
		return None
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def RestartDaemon(self, sender = None, conn = None):
		from subprocess import Popen, PIPE
		command = COMMAND_SERVICE + " laptop-mode restart"
		process = Popen(command.split(), stdout = PIPE, stderr = PIPE)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsAvailable(self, sender = None, conn = None):
		if os.path.exists("/usr/sbin/laptop_mode"):
			self.available = True
		else:
			self.available = False
		return self.available
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetHDPowerMgmt(self, sender = None, conn = None):
		value = self.__read(MAIN_CONFIG_FILE, "BATT_HD_POWERMGMT")
		if value == None:
			return (-1)
		else:
			return int(value)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetConfigFilesControl(self, sender = None, conn = None):
		value = self.__read(CONFIGURATIONFILESCONTROL_CONFIG_FILE, "CONTROL_CONFIG_FILES")
		if value == None:
			return (-1)
		else:
			return int(value)
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetEthernet(self, sender = None, conn = None):
		value = self.__read(ETHERNET_CONFIG_FILE, "CONTROL_ETHERNET")
		if value == None:
			return (-1)
		else:
			return int(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetHalPolling(self, sender = None, conn = None):
		value = self.__read(HALPOLLING_CONFIG_FILE, "CONTROL_HAL_POLLING")
		if value == None:
			return (-1)
		else:
			return int(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetIntelHDAPower(self, sender = None, conn = None):
		value = self.__read(INTELHDAPOWERSAVE_CONFIG_FILE, "CONTROL_INTEL_HDA_POWER")
		if value == None:
			return (-1)
		else:
			return int(value)
		
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetIntelSATAPower(self, sender = None, conn = None):
		value = self.__read(INTELSATAPOWERMGMT_CONFIG_FILE, "CONTROL_INTEL_SATA_POWER")
		if value == None:
			return (-1)
		else:
			return int(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetSchedMcPower(self, sender = None, conn = None):
		value = self.__read(SCHEDMCPOWERSAVINGS_CONFIG_FILE, "CONTROL_SCHED_MC_POWER_SAVINGS")
		if value == None:
			return (-1)
		else:
			return int(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetUSBAutosuspend(self, sender = None, conn = None):
		value = self.__read(USBAUTOSUSPEND_CONFIG_FILE, "CONTROL_USB_AUTOSUSPEND")
		if value == None:
			return (-1)
		else:
			return int(value)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetVideoOutput(self, sender = None, conn = None):
		value = self.__read(VIDEOOUT_CONFIG_FILE, "CONTROL_VIDEO_OUTPUTS")
		if value == None:
			return (-1)
		else:
			return int(value)
		
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetHDPowerMgmt(self, value, sender = None, conn = None):
		if value < 1 or value > 255:
			return False
		return self.__write(MAIN_CONFIG_FILE, "BATT_HD_POWERMGMT", str(value))

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetConfigFilesControl(self, value, sender = None, conn = None):
		if value != 0 and value != 1:
			return False
		return self.__write(CONFIGURATIONFILESCONTROL_CONFIG_FILE, "CONTROL_CONFIG_FILES", str(value))
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetEthernet(self, value, sender = None, conn = None):
		if value != 0 and value != 1:
			return False
		self.__write(ETHERNET_CONFIG_FILE, "ETHERNET_DEVICES", "\"eth0\"")
		return self.__write(ETHERNET_CONFIG_FILE, "CONTROL_ETHERNET", str(value))

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetHalPolling(self, value, sender = None, conn = None):
		if value != 0 and value != 1:
			return False
		return self.__write(HALPOLLING_CONFIG_FILE, "CONTROL_HAL_POLLING", str(value))

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetIntelHDAPower(self, value, sender = None, conn = None):
		if value != 0 and value != 1:
			return False
		return self.__write(INTELHDAPOWERSAVE_CONFIG_FILE, "CONTROL_INTEL_HDA_POWER", str(value))

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetIntelSATAPower(self, value, sender = None, conn = None):
		if value != 0 and value != 1:
			return False
		return self.__write(INTELSATAPOWERMGMT_CONFIG_FILE, "CONTROL_INTEL_SATA_POWER", str(value))

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSchedMcPower(self, value, sender = None, conn = None):
		if value != 0 and value != 1:
			return False
		return self.__write(SCHEDMCPOWERSAVINGS_CONFIG_FILE, "CONTROL_SCHED_MC_POWER_SAVINGS", str(value))

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetUSBAutosuspend(self, value, sender = None, conn = None):
		if value != 0 and value != 1:
			return False
		return self.__write(USBAUTOSUSPEND_CONFIG_FILE, "CONTROL_USB_AUTOSUSPEND", str(value))

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 'i', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetVideoOutput(self, value, sender = None, conn = None):
		if value != 0 and value != 1:
			return False
		self.__write(VIDEOOUT_CONFIG_FILE, "BATT_DISABLE_VIDEO_OUTPUTS", "\"VGA1\"")
		return self.__write(VIDEOOUT_CONFIG_FILE, "CONTROL_VIDEO_OUTPUTS", str(value))
