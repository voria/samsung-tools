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

class Config():
	def __init__(self, configfile):
		self.config = ConfigParser.SafeConfigParser()
		try:
			self.config.readfp(open(configfile))
		except:
			# configfile not found?
			# Use default options
			log_system.write("WARNING: 'Config()' - '" + configfile + "' not found. Using default values for all options.")
			self.config.add_section("Main")
			self.config.set("Main", "WIRELESS_TOGGLE_METHOD", WIRELESS_TOGGLE_METHOD_DEFAULT)
			self.config.set("Main", "WIRELESS_DEVICE", WIRELESS_DEVICE_DEFAULT)
			self.config.set("Main", "WIRELESS_MODULE", WIRELESS_MODULE_DEFAULT)
		# Options sanity check
		if self.config.get("Main", "WIRELESS_TOGGLE_METHOD") not in ["iwconfig", "module", "esdm"]:
			# Option is invalid, set default value
			log_system.write("WARNING: 'Config()' - 'WIRELESS_TOGGLE_METHOD' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + WIRELESS_TOGGLE_METHOD_DEFAULT + "').")
			self.config.set("Main", "WIRELESS_TOGGLE_METHOD", WIRELESS_TOGGLE_METHOD_DEFAULT)
		
	def getWirelessMethod(self):
		return self.config.get("Main", "WIRELESS_TOGGLE_METHOD") 
	
	def getWirelessDevice(self):
		return self.config.get("Main", "WIRELESS_DEVICE")
	
	def getWirelessModule(self):
		return self.config.get("Main", "WIRELESS_MODULE")
		
