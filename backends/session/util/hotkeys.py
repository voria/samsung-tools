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

import os
import shutil
import subprocess

from backends.globals import *

BACKLIGHT_HOTKEY_COMMAND = "samsung-tools -b toggle --show-notify --quiet"
BLUETOOTH_HOTKEY_COMMAND = "samsung-tools -B toggle --show-notify --quiet"
FAN_HOTKEY_COMMAND = "samsung-tools -f hotkey --show-notify --quiet"
WEBCAM_HOTKEY_COMMAND = "samsung-tools -w toggle --show-notify --quiet"
WIRELESS_HOTKEY_COMMAND = "samsung-tools -W toggle --show-notify --quiet"

XBINDKEYS_CONFIG_FILE = os.path.join(os.getenv('HOME'), ".xbindkeysrc")

class Hotkeys():
	def __init__(self):
		# Make sure the xindkeys configuration file exists
		self.__touch_config_file()
		# Add a dummy command to xbindkeys configuration file.
		# If the file is empty, xbindkeys will quit ungracefully.
		self.__update_hotkey("SamsungToolsDummyCommand", "Control+Alt+Shift+Mod4+F1+F2+F3")
		# Set hotkeys
		if sessionconfig.getUseHotkeys() == "true":
			self.setBacklightHotkey(sessionconfig.getBacklightHotkey())
			self.setBluetoothHotkey(sessionconfig.getBluetoothHotkey())
			self.setFanHotkey(sessionconfig.getFanHotkey())
			self.setWebcamHotkey(sessionconfig.getWebcamHotkey())
			self.setWirelessHotkey(sessionconfig.getWirelessHotkey())
			self.__start_daemon() # make sure xbindkeys is started
		else:
			self.setBacklightHotkey("disable")
			self.setBluetoothHotkey("disable")
			self.setFanHotkey("disable")
			self.setWebcamHotkey("disable")
			self.setWirelessHotkey("disable")
	
	def __touch_config_file(self):
		""" Make sure the XBINDKEYS_CONFIG_FILE exists. """
		if not os.path.exists(XBINDKEYS_CONFIG_FILE):
			file = open(XBINDKEYS_CONFIG_FILE, 'w')
			file.close()
	
	def __update_hotkey(self, command, hotkey):
		""" Update the hotkey for 'command' to 'hotkey'. """
		""" If 'command' is not found, add it with the new 'hotkey'. """
		""" Return 'True' on success, 'False' otherwise. """
		self.__touch_config_file()
		oldfile = open(XBINDKEYS_CONFIG_FILE, "r")
		newfile = open(XBINDKEYS_CONFIG_FILE + ".new", "w")
		# Search for command
		commandfound = False
		skipnextline = False
		for line in oldfile:
			if skipnextline == False:
				newfile.write(line)
			else:
				skipnextline = False
			if line == '"' + command + '"\n':
				newfile.write("  " + hotkey + "\n") # update hotkey
				commandfound = True
				skipnextline = True
		if commandfound == False:
			# command not found, add it
			newfile.write('"' + command + '"\n')
			newfile.write("  " + hotkey + "\n")
		oldfile.close()
		newfile.close()
		try:
			os.remove(XBINDKEYS_CONFIG_FILE)
		except:
			sessionlog.write("ERROR: 'Hotkeys.__update_hotkey()' - Cannot replace '" + XBINDKEYS_CONFIG_FILE + "'.")
			os.remove(XBINDKEYS_CONFIG_FILE + ".new")
			return False
		shutil.move(XBINDKEYS_CONFIG_FILE + ".new", XBINDKEYS_CONFIG_FILE)
		return True
	
	def __remove_hotkey(self, command):
		""" Remove the hotkey for 'command' (and 'command' too, of course). """
		""" Return 'True' on success, 'False' otherwise. """
		self.__touch_config_file()
		oldfile = open(XBINDKEYS_CONFIG_FILE, "r")
		newfile = open(XBINDKEYS_CONFIG_FILE + ".new", "w")
		commandfound = False
		skipnextline = False
		for line in oldfile:
			if skipnextline != True:
				if line != '"' + command + '"\n':
					newfile.write(line)
				else:
					commandfound = True
					skipnextline = True
			else:
				skipnextline = False
		oldfile.close()
		newfile.close()
		if commandfound == True:
			try:
				os.remove(XBINDKEYS_CONFIG_FILE)
			except:
				sessionlog.write("ERROR: 'Hotkeys.__remove_hotkey()' - Cannot replace '" + XBINDKEYS_CONFIG_FILE + "'.")
				os.remove(XBINDKEYS_CONFIG_FILE + ".new")
				return False
			shutil.move(XBINDKEYS_CONFIG_FILE + ".new", XBINDKEYS_CONFIG_FILE)
		else:
			os.remove(XBINDKEYS_CONFIG_FILE + ".new")
		return True
	
	def __start_daemon(self):
		""" Start the 'xbindkeys' command line utility, if it's not already running. """
		# Check if xbindkeys is already started
		command = "ps x"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			output = process.communicate()[0].split()
			if "xbindkeys" in output:
				# already enabled
				return
		except:
			sessionlog.write("ERROR: 'Hotkeys.startDaemon()' - COMMAND: '" + command + "' - Exception thrown.")
			return
		command = "xbindkeys"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
		except:
			sessionlog.write("ERROR: 'Hotkeys.startDaemon()' - COMMAND: '" + command + "' - Exception thrown.")
	
	def __config_changed(self):
		""" Force xbindkeys to reload its configuration file. """
		command = "killall -HUP xbindkeys"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
		except:
			sessionlog.write("ERROR: 'Hotkeys.__config_changed()' - COMMAND: '" + command + "' - Exception thrown.")
		
	def setBacklightHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(BACKLIGHT_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(BACKLIGHT_HOTKEY_COMMAND, hotkey) 
			self.__start_daemon() # make sure xbindkeys is started
		self.__config_changed()
		return result
	
	def setBluetoothHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(BLUETOOTH_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(BLUETOOTH_HOTKEY_COMMAND, hotkey)
			self.__start_daemon() # make sure xbindkeys is started
		self.__config_changed()
		return result
	
	def setFanHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(FAN_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(FAN_HOTKEY_COMMAND, hotkey)
			self.__start_daemon() # make sure xbindkeys is started
		self.__config_changed()
		return result
		
	def setWebcamHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(WEBCAM_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(WEBCAM_HOTKEY_COMMAND, hotkey)
			self.__start_daemon() # make sure xbindkeys is started
		self.__config_changed()
		return result
		
	def setWirelessHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(WIRELESS_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(WIRELESS_HOTKEY_COMMAND, hotkey)
			self.__start_daemon() # make sure xbindkeys is started
		self.__config_changed()
		return result
