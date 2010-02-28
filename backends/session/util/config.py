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

LAST_STATUS_RESTORE_DEFAULT = "true"
BACKLIGHT_HOTKEY_DEFAULT = "XF86Launch1"
BLUETOOTH_HOTKEY_DEFAULT = "XF86Launch2"
FAN_HOTKEY_DEFAULT = "XF86Launch3"
WEBCAM_HOTKEY_DEFAULT = "<Shift><Control><Alt>w"
WIRELESS_HOTKEY_DEFAULT = "XF86WLAN"

class SessionConfig():
	def __init__(self, configfile):
		self.config = ConfigParser.SafeConfigParser()
		try:
			self.config.readfp(open(configfile))
		except:
			# configfile not found?
			# Use default options
			log_system.write("WARNING: 'SessionConfig()' - '" + configfile + "' not found. Using default values for all options.")
			self.config.add_section("Main")
			self.config.set("Main", "LAST_STATUS_RESTORE", LAST_STATUS_RESTORE_DEFAULT)
			self.config.set("Main", "BACKLIGHT_HOTKEY", BACKLIGHT_HOTKEY_DEFAULT)
			self.config.set("Main", "BLUETOOTH_HOTKEY", BLUETOOTH_HOTKEY_DEFAULT)
			self.config.set("Main", "FAN_HOTKEY", FAN_HOTKEY_DEFAULT)
			self.config.set("Main", "WEBCAM_HOTKEY", WEBCAM_HOTKEY_DEFAULT)
			self.config.set("Main", "WIRELESS_HOTKEY", WIRELESS_HOTKEY_DEFAULT)
		# Options sanity check
		if self.config.get("Main", "LAST_STATUS_RESTORE") not in ["true", "false"]:
			# Option is invalid, set default value
			log_system.write("WARNING: 'SessionConfig()' - 'LAST_STATUS_RESTORE' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + LAST_STATUS_RESTORE_DEFAULT + "').")
			self.config.set("Main", "LAST_STATUS_RESTORE", LAST_STATUS_RESTORE_DEFAULT)
		
	def getLastStatusRestore(self):
		return self.config.get("Main", "LAST_STATUS_RESTORE") 
	
	def getBacklightHotkey(self):
		return self.config.get("Main", "BACKLIGHT_HOTKEY")
	
	def getBluetoothHotkey(self):
		return self.config.get("Main", "BLUETOOTH_HOTKEY")
	
	def getFanHotkey(self):
		return self.config.get("Main", "FAN_HOTKEY")
	
	def getWebcamHotkey(self):
		return self.config.get("Main", "WEBCAM_HOTKEY")
	
	def getWirelessHotkey(self):
		return self.config.get("Main", "WIRELESS_HOTKEY")
	
	def setBacklightHotkey(self, hotkey):
		self.config.set("Main", "BACKLIGHT_HOTKEY", hotkey)
	
	def setBluetoothHotkey(self, hotkey):
		self.config.set("Main", "BLUETOOTH_HOTKEY", hotkey)
		
	def setFanHotkey(self, hotkey):
		self.config.set("Main", "FAN_HOTKEY", hotkey)
		
	def setWebcamHotkey(self, hotkey):
		self.config.set("Main", "WEBCAM_HOTKEY", hotkey)
		
	def setWirelessHotkey(self, hotkey):
		self.config.set("Main", "WIRELESS_HOTKEY", hotkey)
