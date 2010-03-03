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

from backends.globals import *

WIRELESS_TOGGLE_METHOD_DEFAULT = "iwconfig"
WIRELESS_DEVICE_DEFAULT = "wlan0"
WIRELESS_MODULE_DEFAULT = "ath5k"
LAST_STATUS_RESTORE_DEFAULT = "true"

class SystemConfig():
	def __init__(self, configfile):
		self.configfile = configfile
		self.config = ConfigParser.SafeConfigParser()
		try:
			self.config.readfp(open(configfile))
		except:
			# configfile not found?
			# Use default options
			log_system.write("WARNING: 'SystemConfig()' - '" + configfile + "' not found. Using default values for all options.")
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
		if self.config.get("Main", "WIRELESS_TOGGLE_METHOD") not in ["iwconfig", "module", "esdm"]:
			# Option is invalid, set default value
			log_system.write("WARNING: 'SystemConfig()' - 'WIRELESS_TOGGLE_METHOD' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + WIRELESS_TOGGLE_METHOD_DEFAULT + "').")
			self.config.set("Main", "WIRELESS_TOGGLE_METHOD", WIRELESS_TOGGLE_METHOD_DEFAULT)
		if self.config.get("Main", "LAST_STATUS_RESTORE") not in ["true", "false"]:
			# Option is invalid, set default value
			log_system.write("WARNING: 'SystemConfig()' - 'LAST_STATUS_RESTORE' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + LAST_STATUS_RESTORE_DEFAULT + "').")
			self.config.set("Main", "LAST_STATUS_RESTORE", LAST_STATUS_RESTORE_DEFAULT)
	
	def __write(self):
		""" Write on disk the config file. """
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
			"# Set this to 'false' if you don't want the last status for bluetooth,\n",
			"# webcam and wireless restored after a suspend/hibernate/reboot cycle.\n",
			"LAST_STATUS_RESTORE=%s\n" % self.config.get("Main", "LAST_STATUS_RESTORE")
			]
		with open(self.configfile, "w") as config:
			config.writelines(text)	
	
	def getLastStatusRestore(self):
		return self.config.get("Main", "LAST_STATUS_RESTORE")
	
	def getWirelessToggleMethod(self):
		return self.config.get("Main", "WIRELESS_TOGGLE_METHOD") 
	
	def getWirelessDevice(self):
		return self.config.get("Main", "WIRELESS_DEVICE")
	
	def getWirelessModule(self):
		return self.config.get("Main", "WIRELESS_MODULE")
	
	def setLastStatusRestore(self, value):
		if value == "default": # set default
			value = LAST_STATUS_RESTORE_DEFAULT
		if value != "false" and value != "true":
			return
		self.config.set("Main", "LAST_STATUS_RESTORE", value)
		self.__write()
	
	def setWirelessToggleMethod(self, value):
		if value == "default": # set default
			value = WIRELESS_TOGGLE_METHOD_DEFAULT
		if value != "iwconfig" and value != "module" and value != "esdm":
			return
		self.config.set("Main", "WIRELESS_TOGGLE_METHOD", value)
		self.__write()
	
	def setWirelessDevice(self, value):
		if value == "default": # set default
			value = WIRELESS_DEVICE_DEFAULT
		self.config.set("Main", "WIRELESS_DEVICE", value)
		self.__write()
		
	def setWirelessModule(self, value):
		if value == "default": # set default
			value = WIRELESS_MODULE_DEFAULT
		self.config.set("Main", "WIRELESS_MODULE", value)
		self.__write()
