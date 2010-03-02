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

BACKLIGHT_HOTKEY_DEFAULT = "XF86Launch1"
BLUETOOTH_HOTKEY_DEFAULT = "XF86Launch2"
FAN_HOTKEY_DEFAULT = "XF86Launch3"
WEBCAM_HOTKEY_DEFAULT = "<Shift><Control><Alt>w"
WIRELESS_HOTKEY_DEFAULT = "XF86WLAN"

class SessionConfig():
	def __init__(self, configfile):
		self.config = ConfigParser.SafeConfigParser()
		self.configfile = configfile
		try:
			self.config.readfp(open(configfile))
		except:
			# configfile not found?
			# Use default options
			self.config.add_section("Main")
			self.config.set("Main", "BACKLIGHT_HOTKEY", BACKLIGHT_HOTKEY_DEFAULT)
			self.config.set("Main", "BLUETOOTH_HOTKEY", BLUETOOTH_HOTKEY_DEFAULT)
			self.config.set("Main", "FAN_HOTKEY", FAN_HOTKEY_DEFAULT)
			self.config.set("Main", "WEBCAM_HOTKEY", WEBCAM_HOTKEY_DEFAULT)
			self.config.set("Main", "WIRELESS_HOTKEY", WIRELESS_HOTKEY_DEFAULT)
		# Check if all options are specified in the config file
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
		
	def __write(self):
		""" Write on disk the config file. """
		# We don't use the ConfigParser builtin write function,
		# because it seems to be impossible to add comments to config file.
		text = [
			"#\n",
			"# Configuration file for samsung-tools - session service\n",
			"#\n",
			"\n",
			"[Main]\n",
			"# Hotkeys configuration\n",
			"BACKLIGHT_HOTKEY=%s\n" % self.config.get("Main", "BACKLIGHT_HOTKEY"),
			"BLUETOOTH_HOTKEY=%s\n" % self.config.get("Main", "BLUETOOTH_HOTKEY"),
			"FAN_HOTKEY=%s\n" % self.config.get("Main", "FAN_HOTKEY"),
			"WEBCAM_HOTKEY=%s\n" % self.config.get("Main", "WEBCAM_HOTKEY"),
			"WIRELESS_HOTKEY=%s\n" % self.config.get("Main", "WIRELESS_HOTKEY")
			]	
		with open(self.configfile, "w") as config:
			config.writelines(text)			
	
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
		self.__write()
	
	def setBluetoothHotkey(self, hotkey):
		self.config.set("Main", "BLUETOOTH_HOTKEY", hotkey)
		self.__write()
		
	def setFanHotkey(self, hotkey):
		self.config.set("Main", "FAN_HOTKEY", hotkey)
		self.__write()
		
	def setWebcamHotkey(self, hotkey):
		self.config.set("Main", "WEBCAM_HOTKEY", hotkey)
		self.__write()
		
	def setWirelessHotkey(self, hotkey):
		self.config.set("Main", "WIRELESS_HOTKEY", hotkey)
		self.__write()
