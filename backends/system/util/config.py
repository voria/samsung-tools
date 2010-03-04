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

import ConfigParser

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
		text = [
			"#\n",
			"# Configuration file for samsung-tools - system service\n",
			"#\n",
			"\n",
			"[Main]\n",
			"# Method for enabling/disabling wireless.\n",
			"# Valid values are:\n",
			"# 'iwconfig' - use iwconfig commands\n",
			"# 'module' - use kernel module removal\n",
			"# 'esdm' - use easy-slow-down-manager interface\n"
			"WIRELESS_TOGGLE_METHOD=%s\n" % self.config.get("Main", "WIRELESS_TOGGLE_METHOD"),
			"\n",
			"# Wireless device to control, when WIRELESS_TOGGLE_METHOD=iwconfig\n",
			"WIRELESS_DEVICE=%s\n" % self.config.get("Main", "WIRELESS_DEVICE"),
			"\n",
			"# Kernel module to control, when WIRELESS_TOGGLE_METHOD=module\n",
			"WIRELESS_MODULE=%s\n" % self.config.get("Main", "WIRELESS_MODULE"),
			"\n",
			"# Set this to 'false' if you don't want the last status for devices\n",
			"# to be restored after a suspend/hibernate/reboot cycle.\n",
			"LAST_STATUS_RESTORE=%s\n" % self.config.get("Main", "LAST_STATUS_RESTORE")
			]
		try:
			with open(self.configfile, "w") as config:
				config.writelines(text)
			return True
		except:
			systemlog.write("ERROR: 'SystemConfig().__write()' - cannot write new config file.")
			return False	
	
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
	
