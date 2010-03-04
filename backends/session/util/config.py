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

# Options defaults
USE_HOTKEYS_DEFAULT = "true"
BACKLIGHT_HOTKEY_DEFAULT = "XF86Launch1"
BLUETOOTH_HOTKEY_DEFAULT = "XF86Launch2"
FAN_HOTKEY_DEFAULT = "XF86Launch3"
WEBCAM_HOTKEY_DEFAULT = "<Alt>KP_Insert"
WIRELESS_HOTKEY_DEFAULT = "XF86WLAN"
USE_HOTKEYS_ACCEPTED_VALUES = ['true', 'false']

class SessionConfig():
	""" Manage session service configuration file """
	def __init__(self, configfile):
		self.config = ConfigParser.SafeConfigParser()
		self.configfile = configfile
		try:
			self.config.readfp(open(configfile))
		except:
			# configfile not found?
			# Use default options
			sessionlog.write("WARNING: 'SessionConfig()' - '" + configfile + "' not found. Using default values for all options.")
			self.config.add_section("Main")
			self.config.set("Main", "USE_HOTKEYS", USE_HOTKEYS_DEFAULT)
			self.config.set("Main", "BACKLIGHT_HOTKEY", BACKLIGHT_HOTKEY_DEFAULT)
			self.config.set("Main", "BLUETOOTH_HOTKEY", BLUETOOTH_HOTKEY_DEFAULT)
			self.config.set("Main", "FAN_HOTKEY", FAN_HOTKEY_DEFAULT)
			self.config.set("Main", "WEBCAM_HOTKEY", WEBCAM_HOTKEY_DEFAULT)
			self.config.set("Main", "WIRELESS_HOTKEY", WIRELESS_HOTKEY_DEFAULT)
		# Check if all options are specified in the config file
		try:
			self.config.get("Main", "USE_HOTKEYS")
		except:
			self.config.set("Main", "USE_HOTKEYS", USE_HOTKEYS_DEFAULT)
		try:
			self.config.get("Main", "BACKLIGHT_HOTKEY")
		except:
			self.config.set("Main", "BACKLIGHT_HOTKEY", BACKLIGHT_HOTKEY_DEFAULT)
		try:
			self.config.get("Main", "BLUETOOTH_HOTKEY")
		except:
			self.config.set("Main", "BLUETOOTH_HOTKEY", BLUETOOTH_HOTKEY_DEFAULT)
		try:
			self.config.get("Main", "FAN_HOTKEY")
		except:
			self.config.set("Main", "FAN_HOTKEY", FAN_HOTKEY_DEFAULT)
		try:
			self.config.get("Main", "WEBCAM_HOTKEY")
		except:
			self.config.set("Main", "WEBCAM_HOTKEY", WEBCAM_HOTKEY_DEFAULT)
		try:
			self.config.get("Main", "WIRELESS_HOTKEY")
		except:
			self.config.set("Main", "WIRELESS_HOTKEY", WIRELESS_HOTKEY_DEFAULT)
		# Options sanity check
		if self.config.get("Main", "USE_HOTKEYS") not in USE_HOTKEYS_ACCEPTED_VALUES:
			# Option is invalid, set default value
			sessionlog.write("WARNING: 'SessionConfig()' - 'USE_HOTKEYS' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + USE_HOTKEYS_DEFAULT + "').")
			self.config.set("Main", "USE_HOTKEYS", USE_HOTKEYS_DEFAULT)
		
	def __write(self):
		""" Write on disk the config file. """
		""" Return "True" on success, "False" otherwise. """
		# We don't use the ConfigParser builtin write function,
		# because it seems to be impossible to add comments to config file.
		text = [
			"#\n",
			"# Configuration file for samsung-tools - session service\n",
			"#\n",
			"\n",
			"[Main]\n",
			"# Hotkeys configuration\n",
			"USE_HOTKEYS=%s\n" % self.config.get("Main", "USE_HOTKEYS"),
			"BACKLIGHT_HOTKEY=%s\n" % self.config.get("Main", "BACKLIGHT_HOTKEY"),
			"BLUETOOTH_HOTKEY=%s\n" % self.config.get("Main", "BLUETOOTH_HOTKEY"),
			"FAN_HOTKEY=%s\n" % self.config.get("Main", "FAN_HOTKEY"),
			"WEBCAM_HOTKEY=%s\n" % self.config.get("Main", "WEBCAM_HOTKEY"),
			"WIRELESS_HOTKEY=%s\n" % self.config.get("Main", "WIRELESS_HOTKEY")
			]
		try:
			with open(self.configfile, "w") as config:
				config.writelines(text)
			return True
		except:
			sessionlog.write("ERROR: 'SessionConfig().__write()' - cannot write new config file.")
			return False
	
	def getUseHotkeys(self):
		""" Return the USE_HOTKEYS option. """
		return self.config.get("Main", "USE_HOTKEYS")
	
	def getBacklightHotkey(self):
		""" Return the BACKLIGHT_HOTKEY option. """
		return self.config.get("Main", "BACKLIGHT_HOTKEY")
	
	def getBluetoothHotkey(self):
		""" Return the BLUETOOTH_HOTKEY option. """
		return self.config.get("Main", "BLUETOOTH_HOTKEY")
	
	def getFanHotkey(self):
		""" Return the FAN_HOTKEY option. """
		return self.config.get("Main", "FAN_HOTKEY")
	
	def getWebcamHotkey(self):
		""" Return the WEBCAM_HOTKEY option. """
		return self.config.get("Main", "WEBCAM_HOTKEY")
	
	def getWirelessHotkey(self):
		""" Return the WIRELESS_HOTKEY option. """
		return self.config.get("Main", "WIRELESS_HOTKEY")
	
	def setUseHotkeys(self, value):
		""" Set the USE_HOTKEYS option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = USE_HOTKEYS_DEFAULT
		if value not in USE_HOTKEYS_ACCEPTED_VALUES:
			return False
		self.config.set("Main", "USE_HOTKEYS", value)
		return self.__write()
	
	def setBacklightHotkey(self, hotkey):
		""" Set the BACKLIGHT_HOTKEY option. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "default": # set default
			hotkey = BACKLIGHT_HOTKEY_DEFAULT
		self.config.set("Main", "BACKLIGHT_HOTKEY", hotkey)
		return self.__write()
	
	def setBluetoothHotkey(self, hotkey):
		""" Set the BLUETOOTH_HOTKEY option. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "default": # set default
			hotkey = BLUETOOTH_HOTKEY_DEFAULT
		self.config.set("Main", "BLUETOOTH_HOTKEY", hotkey)
		return self.__write()
		
	def setFanHotkey(self, hotkey):
		""" Set the FAN_HOTKEY option. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "default": # set default
			hotkey = FAN_HOTKEY_DEFAULT
		self.config.set("Main", "FAN_HOTKEY", hotkey)
		return self.__write()
		
	def setWebcamHotkey(self, hotkey):
		""" Set the WEBCAM_HOTKEY option. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "default": # set default
			hotkey = WEBCAM_HOTKEY_DEFAULT
		self.config.set("Main", "WEBCAM_HOTKEY", hotkey)
		return self.__write()
		
	def setWirelessHotkey(self, hotkey):
		""" Set the WIRELESS_HOTKEY option. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "default": # set default
			hotkey = WIRELESS_HOTKEY_DEFAULT
		self.config.set("Main", "WIRELESS_HOTKEY", hotkey)
		return self.__write()
