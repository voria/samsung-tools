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

BACKLIGHT_HOTKEY_COMMAND = "samsung-tools --show-notify --quiet --backlight hotkey"
BLUETOOTH_HOTKEY_COMMAND = "samsung-tools --show-notify --quiet --bluetooth hotkey"
CPU_HOTKEY_COMMAND = "samsung-tools --show-notify --quiet --cpu hotkey"
WEBCAM_HOTKEY_COMMAND = "samsung-tools --show-notify --quiet --webcam hotkey"
WIRELESS_HOTKEY_COMMAND = "samsung-tools --show-notify --quiet --wireless hotkey"
DUMMY_HOTKEY_COMMAND = "SamsungToolsDummyCommand"
DUMMY_HOTKEY = "Control+Alt+Shift+Mod4+F1+F2+F3"

XBINDKEYS_CONFIG_FILE = os.path.join(os.getenv('HOME'), ".xbindkeysrc")

class Hotkeys():
	def __init__(self):
		# Make sure the xindkeys configuration file exists
		self.__touch_config_file()
		# Add a dummy command to xbindkeys configuration file.
		# This is needed because if the file is empty, xbindkeys will kill itself ungracefully.
		self.__update_hotkey(DUMMY_HOTKEY_COMMAND, DUMMY_HOTKEY)
		# Set hotkeys
		if sessionconfig.getUseHotkeys() == "true":
			self.setBacklightHotkey(sessionconfig.getBacklightHotkey())
			self.setBluetoothHotkey(sessionconfig.getBluetoothHotkey())
			self.setCpuHotkey(sessionconfig.getCpuHotkey())
			self.setWebcamHotkey(sessionconfig.getWebcamHotkey())
			self.setWirelessHotkey(sessionconfig.getWirelessHotkey())
		else:
			self.setBacklightHotkey("disable")
			self.setBluetoothHotkey("disable")
			self.setCpuHotkey("disable")
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

	def __stop_daemon(self):
		""" Stop all running xbindkeys instances. """
		# stop all xbindkeys running instances
		returncode = 0
		command = "killall xbindkeys"
		while returncode == 0:
			try:
				process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				process.communicate()
				returncode = process.returncode
			except:
				sessionlog.write("ERROR: 'Hotkeys.__stop_daemon()' - COMMAND: '" + command + "' - Exception thrown.")
				return

	def __restart_daemon(self):
		""" Restart xbindkeys to reload its configuration file. """
		""" This is needed because sometimes xbindkeys fails to activate new keys. """
		""" Note: xbindkeys is actually restarted only if its configuration file """
		""" is not empty (apart for the dummy command). """
		self.__stop_daemon()
		# start it again only if needed
		file = open(XBINDKEYS_CONFIG_FILE)
		content = file.readlines()
		file.close()
		if len(content) == 2 and \
		content[0].strip('\n "') == DUMMY_HOTKEY_COMMAND and \
		content[1].strip() == DUMMY_HOTKEY:
			return
		# File is not empty, restart it
		command = "xbindkeys"
		try:
			process = subprocess.Popen(command.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			process.communicate()
		except:
			sessionlog.write("ERROR: 'Hotkeys.__restart_daemon()' - COMMAND: '" + command + "' - Exception thrown.")

	def setBacklightHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(BACKLIGHT_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(BACKLIGHT_HOTKEY_COMMAND, hotkey)
		self.__restart_daemon()
		return result

	def setBluetoothHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(BLUETOOTH_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(BLUETOOTH_HOTKEY_COMMAND, hotkey)
		self.__restart_daemon()
		return result

	def setCpuHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(CPU_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(CPU_HOTKEY_COMMAND, hotkey)
		self.__restart_daemon()
		return result

	def setWebcamHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(WEBCAM_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(WEBCAM_HOTKEY_COMMAND, hotkey)
		self.__restart_daemon()
		return result

	def setWirelessHotkey(self, hotkey):
		""" Set the new hotkey. """
		""" Return 'True' on success, 'False' otherwise. """
		if hotkey == "disable":
			result = self.__remove_hotkey(WIRELESS_HOTKEY_COMMAND)
		else:
			result = self.__update_hotkey(WIRELESS_HOTKEY_COMMAND, hotkey)
		self.__restart_daemon()
		return result
