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

BACKLIGHT_COMMAND = "samsung-tools -b toggle --show-notify"
BLUETOOTH_COMMAND = "samsung-tools -B toggle --show-notify"
FAN_COMMAND = "samsung-tools -f hotkey --show-notify"
WEBCAM_COMMAND = "samsung-tools -w toggle --show-notify"
WIRELESS_COMMAND = "samsung-tools -W toggle --show-notify"

BACKLIGHT_HOTKEY_DEFAULT = "XF86Launch1"
BLUETOOTH_HOTKEY_DEFAULT = "XF86Launch2"
FAN_HOTKEY_DEFAULT = "XF86Launch3"
WEBCAM_HOTKEY_DEFAULT = "Alt + KP_Insert"
WIRELESS_HOTKEY_DEFAULT = "XF86WLAN"

XBINDKEYS_CONFIG_FILE = os.path.join(os.getenv('HOME'), ".xbindkeysrc")

class Hotkeys():
	def __init__(self):
		if not os.path.exists(XBINDKEYS_CONFIG_FILE):
			# Create the configuration file
			file = open(XBINDKEYS_CONFIG_FILE, 'w')
			file.close()
			# Set default hotkeys
			self.setBacklightHotkey("default")
			self.setBluetoothHotkey("default")
			self.setFanHotkey("default")
			self.setWebcamHotkey("default")
			self.setWirelessHotkey("default")
	
	def __get_hotkey(self, command):
		""" Return the hotkey for 'command', 'None' if not found. """
		hotkey = None
		found = False
		file = open(XBINDKEYS_CONFIG_FILE, "r")
		for line in file:
			if found == True:
				hotkey = line.strip()
				break
			if line == '"' + command + '"\n':
				found = True
		file.close()
		return hotkey
	
	def __update_hotkey(self, command, hotkey):
		""" Update the hotkey for 'command' to 'hotkey'. """
		""" If 'command' is not found, add it with the new 'hotkey'. """
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
		os.remove(XBINDKEYS_CONFIG_FILE)
		shutil.move(XBINDKEYS_CONFIG_FILE + ".new", XBINDKEYS_CONFIG_FILE)
	
	def startHotkeys(self):
		# Check if xbindkeys is already started
		process = subprocess.Popen(['ps', 'x'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		output = process.communicate()[0].split()
		if "xbindkeys" in output:
			# already enabled
			return
		process = subprocess.Popen(['xbindkeys'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		process.communicate()
	
	def stopHotkeys(self):
		process = subprocess.Popen(['killall', 'xbindkeys'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		process.communicate()
	
	def restartHotkeys(self):
		self.disableHotkeys()
		self.enableHotkeys()
	
	def getBacklightHotkey(self):
		return self.__get_hotkey(BACKLIGHT_COMMAND)
	
	def getBluetoothHotkey(self):
		return self.__get_hotkey(BLUETOOTH_COMMAND)
	
	def getFanHotkey(self):
		return self.__get_hotkey(FAN_COMMAND)
	
	def getWebcamHotkey(self):
		return self.__get_hotkey(WEBCAM_COMMAND)
	
	def getWirelessHotkey(self):
		return self.__get_hotkey(WIRELESS_COMMAND)
	
	def setBacklightHotkey(self, hotkey):
		if hotkey == "default":
			hotkey = BACKLIGHT_HOTKEY_DEFAULT
		self.__update_hotkey(BACKLIGHT_COMMAND, hotkey)
	
	def setBluetoothHotkey(self, hotkey):
		if hotkey == "default":
			hotkey = BLUETOOTH_HOTKEY_DEFAULT
		self.__update_hotkey(BLUETOOTH_COMMAND, hotkey)
	
	def setFanHotkey(self, hotkey):
		if hotkey == "default":
			hotkey = FAN_HOTKEY_DEFAULT
		self.__update_hotkey(FAN_COMMAND, hotkey)
		
	def setWebcamHotkey(self, hotkey):
		if hotkey == "default":
			hotkey = WEBCAM_HOTKEY_DEFAULT
		self.__update_hotkey(WEBCAM_COMMAND, hotkey)
		
	def setWirelessHotkey(self, hotkey):
		if hotkey == "default":
			hotkey = WIRELESS_HOTKEY_DEFAULT
		self.__update_hotkey(WIRELESS_COMMAND, hotkey)

