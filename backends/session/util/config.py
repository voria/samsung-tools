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
		# Check if all options are specified in the config file
		try:
			self.config.get("Main", "USE_HOTKEYS")
		except:
			self.config.set("Main", "USE_HOTKEYS", USE_HOTKEYS_DEFAULT)
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
	
	def setUseHotkeys(self, value):
		""" Set the USE_HOTKEYS option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = USE_HOTKEYS_DEFAULT
		if value not in USE_HOTKEYS_ACCEPTED_VALUES:
			return False
		self.config.set("Main", "USE_HOTKEYS", value)
		return self.__write()
