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
import ConfigParser

from backends.globals import *

# Options defaults
WIRELESS_TOGGLE_METHOD_DEFAULT = "iwconfig"
WIRELESS_DEVICE_DEFAULT = "wlan0"
WIRELESS_MODULE_DEFAULT = "ath5k"
LAST_STATUS_RESTORE_DEFAULT = "true"
WIRELESS_TOGGLE_METHOD_ACCEPTED_VALUES = ['iwconfig', 'module', 'esdm']
LAST_STATUS_RESTORE_ACCEPTED_VALUES = ['true', 'false']

class SystemConfig():
	""" Manage system service configuration file """
	def __init__(self, configfile):
		self.configfile = configfile
		self.config = ConfigParser.SafeConfigParser()
		try:
			self.config.readfp(open(configfile))
		except:
			# configfile not found?
			# Use default options
			systemlog.write("WARNING: 'SystemConfig()' - '" + configfile + "' not found. Using default values for all options.")
			self.config.add_section("Main")
			self.config.set("Main", "WIRELESS_TOGGLE_METHOD", WIRELESS_TOGGLE_METHOD_DEFAULT)
			self.config.set("Main", "WIRELESS_DEVICE", WIRELESS_DEVICE_DEFAULT)
			self.config.set("Main", "WIRELESS_MODULE", WIRELESS_MODULE_DEFAULT)
			self.config.set("Main", "LAST_STATUS_RESTORE", LAST_STATUS_RESTORE_DEFAULT)
		# Check if all options are specified in the config file
		else:
			try:
				self.config.get("Main", "WIRELESS_TOGGLE_METHOD")
			except:
				self.config.set("Main", "WIRELESS_TOGGLE_METHOD", WIRELESS_TOGGLE_METHOD_DEFAULT)
			try:
				self.config.get("Main", "WIRELESS_DEVICE")
			except:
				self.config.set("Main", "WIRELESS_DEVICE", WIRELESS_DEVICE_DEFAULT)
			try:
				self.config.get("Main", "WIRELESS_MODULE")
			except:
				self.config.set("Main", "WIRELESS_MODULE", WIRELESS_MODULE_DEFAULT)
			try:
				self.config.get("Main", "LAST_STATUS_RESTORE")
			except:
				self.config.set("Main", "LAST_STATUS_RESTORE", LAST_STATUS_RESTORE_DEFAULT)
		# Options sanity check
		if self.config.get("Main", "WIRELESS_TOGGLE_METHOD") not in WIRELESS_TOGGLE_METHOD_ACCEPTED_VALUES:
			# Option is invalid, set default value
			systemlog.write("WARNING: 'SystemConfig()' - 'WIRELESS_TOGGLE_METHOD' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + WIRELESS_TOGGLE_METHOD_DEFAULT + "').")
			self.config.set("Main", "WIRELESS_TOGGLE_METHOD", WIRELESS_TOGGLE_METHOD_DEFAULT)
		if self.config.get("Main", "LAST_STATUS_RESTORE") not in LAST_STATUS_RESTORE_ACCEPTED_VALUES:
			# Option is invalid, set default value
			systemlog.write("WARNING: 'SystemConfig()' - 'LAST_STATUS_RESTORE' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + LAST_STATUS_RESTORE_DEFAULT + "').")
			self.config.set("Main", "LAST_STATUS_RESTORE", LAST_STATUS_RESTORE_DEFAULT)
	
	def __write(self):
		""" Write on disk the config file. """
		""" Return "True" on success, "False" otherwise. """
		# We don't use the ConfigParser builtin write function,
		# because it seems to be impossible to add comments to config file.
		try:
			oldfile = open(self.configfile, "r")
		except:
			systemlog.write("ERROR: 'SystemConfig().__write()' - '" + self.configfile + "' not found.")
			return False
		try:
			newfile = open(self.configfile + ".new", "w")
		except:
			systemlog.write("ERROR: 'SystemConfig().__write()' - cannot write new config file.")
			oldfile.close()
			return False
		for line in oldfile:
			if line[0:1] == "#" or line == "\n" or line == "[Main]\n":
				newfile.write(line)
			else:
				option = line.split('=')[0].strip()
				try:
					value = self.config.get("Main", option)
					newfile.write(option + "=" + self.config.get("Main", option) + "\n")
				except:
					pass # invalid option, omit it
		oldfile.close()
		newfile.close()
		try:
			os.remove(self.configfile)
		except:
			systemlog.write("ERROR: 'SystemConfig().__write()' - cannot replace old '" + self.configfile + "' with the new version.")
			os.remove(self.configfile + ".new")
			return False
		shutil.move(self.configfile + ".new", self.configfile)
		return True
	
	def getLastStatusRestore(self):
		""" Return the LAST_STATUS_RESTORE option. """
		return self.config.get("Main", "LAST_STATUS_RESTORE")
	
	def getWirelessToggleMethod(self):
		""" Return the WIRELESS_TOGGLE_METHOD option. """
		return self.config.get("Main", "WIRELESS_TOGGLE_METHOD") 
	
	def getWirelessDevice(self):
		""" Return the WIRELESS_DEVICE option. """
		return self.config.get("Main", "WIRELESS_DEVICE")
	
	def getWirelessModule(self):
		""" Return the WIRELESS_MODULE option. """
		return self.config.get("Main", "WIRELESS_MODULE")
	
	def setLastStatusRestore(self, value):
		""" Set the LAST_STATUS_RESTORE option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = LAST_STATUS_RESTORE_DEFAULT
		if value not in LAST_STATUS_RESTORE_ACCEPTED_VALUES:
			return False
		self.config.set("Main", "LAST_STATUS_RESTORE", value)
		return self.__write()
	
	def setWirelessToggleMethod(self, value):
		""" Set the WIRELESS_TOGGLE_METHOD option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = WIRELESS_TOGGLE_METHOD_DEFAULT
		if value not in WIRELESS_TOGGLE_METHOD_ACCEPTED_VALUES:
			return False
		self.config.set("Main", "WIRELESS_TOGGLE_METHOD", value)
		return self.__write()
	
	def setWirelessDevice(self, value):
		""" Set the WIRELESS_DEVICE option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = WIRELESS_DEVICE_DEFAULT
		self.config.set("Main", "WIRELESS_DEVICE", value)
		return self.__write()
		
	def setWirelessModule(self, value):
		""" Set the WIRELESS_MODULE option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = WIRELESS_MODULE_DEFAULT
		self.config.set("Main", "WIRELESS_MODULE", value)
		return self.__write()
	
