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
BLUETOOTH_INITIAL_STATUS_DEFAULT = "last"
WEBCAM_INITIAL_STATUS_DEFAULT = "last"
WIRELESS_INITIAL_STATUS_DEFAULT = "last"
CPUFAN_INITIAL_STATUS_DEFAULT = "normal"
BLUETOOTH_INITIAL_STATUS_ACCEPTED_VALUES = ['on', 'off', 'last']
WEBCAM_INITIAL_STATUS_ACCEPTED_VALUES = ['on', 'off', 'last']
WIRELESS_INITIAL_STATUS_ACCEPTED_VALUES = ['on', 'off', 'last']
CPUFAN_INITIAL_STATUS_ACCEPTED_VALUES = ['normal', 'silent', 'speed', 'last']

class SystemConfig():
	""" Manage system service configuration file """
	def __init__(self, configfile):
		self.configfile = configfile
		self.config = ConfigParser.SafeConfigParser()
		try:
			self.config.readfp(open(configfile, "r"))
		except:
			# configfile not found?
			# Use default options
			systemlog.write("WARNING: 'SystemConfig' - Cannot read '" + configfile + "'. Using default values for all options.")
			self.config.add_section("Main")
			self.config.set("Main", "BLUETOOTH_INITIAL_STATUS", BLUETOOTH_INITIAL_STATUS_DEFAULT)
			self.config.set("Main", "WEBCAM_INITIAL_STATUS", WEBCAM_INITIAL_STATUS_DEFAULT)
			self.config.set("Main", "WIRELESS_INITIAL_STATUS", WIRELESS_INITIAL_STATUS_DEFAULT)
			self.config.set("Main", "CPUFAN_INITIAL_STATUS", CPUFAN_INITIAL_STATUS_DEFAULT)
		# Check if all options are specified in the config file
		else:
			if not self.config.has_section("Main"):
				self.config.add_section("Main")
			try:
				self.config.get("Main", "BLUETOOTH_INITIAL_STATUS")
			except:
				self.config.set("Main", "BLUETOOTH_INITIAL_STATUS", BLUETOOTH_INITIAL_STATUS_DEFAULT)
			try:
				self.config.get("Main", "WEBCAM_INITIAL_STATUS")
			except:
				self.config.set("Main", "WEBCAM_INITIAL_STATUS", WEBCAM_INITIAL_STATUS_DEFAULT)
			try:
				self.config.get("Main", "WIRELESS_INITIAL_STATUS")
			except:
				self.config.set("Main", "WIRELESS_INITIAL_STATUS", WIRELESS_INITIAL_STATUS_DEFAULT)
			try:
				self.config.get("Main", "CPUFAN_INITIAL_STATUS")
			except:
				self.config.set("Main", "CPUFAN_INITIAL_STATUS", CPUFAN_INITIAL_STATUS_DEFAULT)
		# Options sanity check
		if self.config.get("Main", "BLUETOOTH_INITIAL_STATUS") not in BLUETOOTH_INITIAL_STATUS_ACCEPTED_VALUES:
			# Option is invalid, set default value
			systemlog.write("WARNING: 'SystemConfig' - 'BLUETOOTH_INITIAL_STATUS' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + BLUETOOTH_INITIAL_STATUS_DEFAULT + "').")
			self.config.set("Main", "BLUETOOTH_INITIAL_STATUS", BLUETOOTH_INITIAL_STATUS_DEFAULT)
		if self.config.get("Main", "WEBCAM_INITIAL_STATUS") not in WEBCAM_INITIAL_STATUS_ACCEPTED_VALUES:
			# Option is invalid, set default value
			systemlog.write("WARNING: 'SystemConfig' - 'WEBCAM_INITIAL_STATUS' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + WEBCAM_INITIAL_STATUS_DEFAULT + "').")
			self.config.set("Main", "WIRELESS_INITIAL_STATUS", WIRELESS_INITIAL_STATUS_DEFAULT)
		if self.config.get("Main", "WIRELESS_INITIAL_STATUS") not in WIRELESS_INITIAL_STATUS_ACCEPTED_VALUES:
			# Option is invalid, set default value
			systemlog.write("WARNING: 'SystemConfig' - 'WIRELESS_INITIAL_STATUS' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + WIRELESS_INITIAL_STATUS_DEFAULT + "').")
			self.config.set("Main", "WIRELESS_INITIAL_STATUS", WIRELESS_INITIAL_STATUS_DEFAULT)
		if self.config.get("Main", "CPUFAN_INITIAL_STATUS") not in CPUFAN_INITIAL_STATUS_ACCEPTED_VALUES:
			# Option is invalid, set default value
			systemlog.write("WARNING: 'SystemConfig' - 'CPUFAN_INITIAL_STATUS' option specified in '" + configfile + 
					"' is invalid. Using default value ('" + CPUFAN_INITIAL_STATUS_DEFAULT + "').")
			self.config.set("Main", "CPUFAN_INITIAL_STATUS", CPUFAN_INITIAL_STATUS_DEFAULT)
	
	def __write(self, option):
		""" Write the new 'option' in the config file. """
		""" If 'option' does not exists in file, add it. """
		""" Return "True" on success, "False" otherwise. """
		# We don't use the ConfigParser builtin write function,
		# because it seems to be impossible to add comments to config file.
		value = self.config.get("Main", option)
		optionfound = False
		sectionfound = False
		try:
			oldfile = open(self.configfile, "r")
		except:
			systemlog.write("WARNING: 'SystemConfig.__write()' - '" + self.configfile + "' not found. Creating a new one.")
			try:
				oldfile = open(self.configfile, "w").close()
				oldfile = open(self.configfile, "r")
			except:
				systemlog.write("ERROR: 'SystemConfig.__write()' - cannot write the config file.")
				return False
		try:
			newfile = open(self.configfile + ".new", "w")
		except:
			systemlog.write("ERROR: 'SystemConfig.__write()' - cannot write the new config file.")
			oldfile.close()
			return False
		for line in oldfile:
			if line[0:1] == "#" or line == "\n":
				newfile.write(line)
			elif line == "[Main]\n":
				newfile.write(line)
				sectionfound = True
			else:
				currentoption = line.split('=')[0].strip()
				if currentoption != option: # not the option we are searching for
					newfile.write(line)
				else:
					optionfound = True
					try:					
						newfile.write(option + "=" + value + "\n")
					except:
						systemlog.write("ERROR: 'SystemConfig.__write()' - cannot write the new value for '" + option + "' in the new config file.")
						oldfile.close()
						newfile.close()
						os.remove(self.configfile + ".new")
						return False
		oldfile.close()
		if sectionfound == False: # probably an empty file, write section
			newfile.write("[Main]\n")
		if optionfound == False: # option not found in current config file, add it
			newfile.write(option + "=" + value + "\n")
		newfile.close()
		try:
			os.remove(self.configfile)
		except:
			systemlog.write("ERROR: 'SystemConfig.__write()' - cannot replace old '" + self.configfile + "' with the new version.")
			os.remove(self.configfile + ".new")
			return False
		shutil.move(self.configfile + ".new", self.configfile)
		return True
	
	def getBluetoothInitialStatus(self):
		""" Return the BLUETOOTH_INITIAL_STATUS option. """
		return self.config.get("Main", "BLUETOOTH_INITIAL_STATUS")
	
	def getWebcamInitialStatus(self):
		""" Return the WEBCAM_INITIAL_STATUS option. """
		return self.config.get("Main", "WEBCAM_INITIAL_STATUS")
	
	def getWirelessInitialStatus(self):
		""" Return the WIRELESS_INITIAL_STATUS option. """
		return self.config.get("Main", "WIRELESS_INITIAL_STATUS")
	
	def getCpufanInitialStatus(self):
		""" Return the CPUFAN_INITIAL_STATUS option. """
		return self.config.get("Main", "CPUFAN_INITIAL_STATUS")
	
	def setBluetoothInitialStatus(self, value):
		""" Set the BLUETOOTH_INITIAL_STATUS option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = BLUETOOTH_INITIAL_STATUS_DEFAULT
		if value not in BLUETOOTH_INITIAL_STATUS_ACCEPTED_VALUES:
			return False
		self.config.set("Main", "BLUETOOTH_INITIAL_STATUS", value)
		return self.__write("BLUETOOTH_INITIAL_STATUS")
	
	def setWebcamInitialStatus(self, value):
		""" Set the WEBCAM_INITIAL_STATUS option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = WEBCAM_INITIAL_STATUS_DEFAULT
		if value not in WEBCAM_INITIAL_STATUS_ACCEPTED_VALUES:
			return False
		self.config.set("Main", "WEBCAM_INITIAL_STATUS", value)
		return self.__write("WEBCAM_INITIAL_STATUS")
	
	def setWirelessInitialStatus(self, value):
		""" Set the WIRELESS_INITIAL_STATUS option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = WIRELESS_INITIAL_STATUS_DEFAULT
		if value not in WIRELESS_INITIAL_STATUS_ACCEPTED_VALUES:
			return False
		self.config.set("Main", "WIRELESS_INITIAL_STATUS", value)
		return self.__write("WIRELESS_INITIAL_STATUS")
	
	def setCpufanInitialStatus(self, value):
		""" Set the CPUFAN_INITIAL_STATUS option. """
		""" Return 'True' on success, 'False' otherwise. """
		if value == "default": # set default
			value = CPUFAN_INITIAL_STATUS_DEFAULT
		if value not in CPUFAN_INITIAL_STATUS_ACCEPTED_VALUES:
			return False
		self.config.set("Main", "CPUFAN_INITIAL_STATUS", value)
		return self.__write("CPUFAN_INITIAL_STATUS")
