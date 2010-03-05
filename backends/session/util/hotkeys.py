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

BACKLIGHT_HOTKEY_COMMAND = "samsung-tools -b toggle --show-notify"
BLUETOOTH_HOTKEY_COMMAND = "samsung-tools -B toggle --show-notify"
FAN_HOTKEY_COMMAND = "samsung-tools -f hotkey --show-notify"
WEBCAM_HOTKEY_COMMAND = "samsung-tools -w toggle --show-notify"
WIRELESS_HOTKEY_COMMAND = "samsung-tools -W toggle --show-notify"

XBINDKEYS_CONFIG_FILE = os.path.join(os.getenv('HOME'), ".xbindkeysrc")

class Hotkeys():
	def __init__(self):
		# Make sure the xindkeys configuration file exists
		self.__touch_config_file()
		# Set hotkeys
		if sessionconfig.getUseHotkeys() == "true":
			self.setBacklightHotkey(sessionconfig.getBacklightHotkey())
			self.setBluetoothHotkey(sessionconfig.getBluetoothHotkey())
			self.setFanHotkey(sessionconfig.getFanHotkey())
			self.setWebcamHotkey(sessionconfig.getWebcamHotkey())
			self.setWirelessHotkey(sessionconfig.getWirelessHotkey())
			self.restartDaemon()
		else:
			self.setBacklightHotkey("disable")
			self.setBluetoothHotkey("disable")
			self.setFanHotkey("disable")
			self.setWebcamHotkey("disable")
			self.setWirelessHotkey("disable")
			self.stopDaemon()
	
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
		return True
	
	def startDaemon(self):
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
			return
		
	def stopDaemon(self):
		""" Stop the 'xbindkeys' command line utility. """
		command = "killall xbindkeys"
		returncode = 0
		try:
			while returncode == 0:
				process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				process.communicate()
				returncode = process.returncode
		except:
			sessionlog.write("ERROR: 'Hotkeys.stopDaemon()' - COMMAND: '" + command + "' - Exception thrown.")
			return
	
	def restartDaemon(self):
		""" Restart the 'xbindkeys' command line utility. """
		self.stopDaemon()
		self.startDaemon()
	
	def setBacklightHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			return self.__remove_hotkey(BACKLIGHT_HOTKEY_COMMAND)
		else:
			return self.__update_hotkey(BACKLIGHT_HOTKEY_COMMAND, hotkey)
	
	def setBluetoothHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			return self.__remove_hotkey(BLUETOOTH_HOTKEY_COMMAND)
		else:
			return self.__update_hotkey(BLUETOOTH_HOTKEY_COMMAND, hotkey)
	
	def setFanHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			return self.__remove_hotkey(FAN_HOTKEY_COMMAND)
		else:
			return self.__update_hotkey(FAN_HOTKEY_COMMAND, hotkey)
		
	def setWebcamHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			return self.__remove_hotkey(WEBCAM_HOTKEY_COMMAND)
		else:
			return self.__update_hotkey(WEBCAM_HOTKEY_COMMAND, hotkey)
		
	def setWirelessHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			return self.__remove_hotkey(WIRELESS_HOTKEY_COMMAND)
		else:
			return self.__update_hotkey(WIRELESS_HOTKEY_COMMAND, hotkey)
