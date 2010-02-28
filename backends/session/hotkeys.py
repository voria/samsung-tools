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

import gconf

import dbus.service

from backends.globals import *
from backends.session.util.config import SessionConfig

GCONF_KEY_COMMAND = "/apps/metacity/keybinding_commands/command_"
GCONF_KEY_COMMAND_SCHEMA = "/schemas/apps/metacity/keybinding_commands/command"
BACKLIGHT_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "8"
BLUETOOTH_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "9"
FAN_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "10"
WEBCAM_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "11"
WIRELESS_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "12"

GCONF_KEY_RUN = "/apps/metacity/global_keybindings/run_command_"
GCONF_KEY_RUN_SCHEMA = "/schemas/apps/metacity/global_keybindings/run_command"
BACKLIGHT_GCONF_KEY_RUN = GCONF_KEY_RUN + "8"
BLUETOOTH_GCONF_KEY_RUN = GCONF_KEY_RUN + "9"
FAN_GCONF_KEY_RUN = GCONF_KEY_RUN + "10"
WEBCAM_GCONF_KEY_RUN = GCONF_KEY_RUN + "11"
WIRELESS_GCONF_KEY_RUN = GCONF_KEY_RUN + "12"

class Hotkeys(dbus.service.Object):
	""" Control hotkeys """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		config = SessionConfig(USER_CONFIG_FILE)
		self.backlight = config.getBacklightHotkey()
		self.bluetooth = config.getBluetoothHotkey()
		self.fan = config.getFanHotkey()
		self.webcam = config.getWebcamHotkey()
		self.wireless = config.getWirelessHotkey()
		## Set hotkeys in gconf
		gconf_client = gconf.client_get_default()
		gconf_client.set_string(BACKLIGHT_GCONF_KEY_COMMAND, "samsung-tools -b toggle --show-notify")
		gconf_client.set_string(BACKLIGHT_GCONF_KEY_RUN, self.backlight)
		gconf_client.set_string(BLUETOOTH_GCONF_KEY_COMMAND, "samsung-tools -B toggle --show-notify")
		gconf_client.set_string(BLUETOOTH_GCONF_KEY_RUN, self.bluetooth)
		gconf_client.set_string(FAN_GCONF_KEY_COMMAND, "samsung-tools -f cycle --show-notify")
		gconf_client.set_string(FAN_GCONF_KEY_RUN, self.fan)
		gconf_client.set_string(WEBCAM_GCONF_KEY_COMMAND, "samsung-tools -w toggle --show-notify")
		gconf_client.set_string(WEBCAM_GCONF_KEY_RUN, self.webcam)
		gconf_client.set_string(WIRELESS_GCONF_KEY_COMMAND, "samsung-tools -W toggle --show-notify")
		gconf_client.set_string(WIRELESS_GCONF_KEY_RUN, self.wireless)
	
	def GetBacklight(self):
		return self.backlight
	
	def GetBluetooth(self):
		return self.bluetooth
	
	def GetFan(self):
		return self.fan
	
	def GetWebcam(self):
		return self.webcam
	
	def GetWireless(self):
		return self.wireless 
	
	def SetBacklight(self, hotkey):
		self.backlight = hotkey
		config.setBacklightHotkey(hotkey)
		# Update hotkey in gconf
		gconf_client = gconf.client_get_default()
		gconf_client.set_string(BACKLIGHT_GCONF_KEY_RUN, hotkey)

	def SetBluetooth(self, hotkey):
		self.bluetooth = hotkey
		config.setBluetoothHotkey(hotkey)
		# Update hotkey in gconf
		gconf_client = gconf.client_get_default()
		gconf_client.set_string(BLUETOOTH_GCONF_KEY_RUN, hotkey)
	
	def SetFan(self, hotkey):
		self.fan = hotkey
		config.setFanHotkey(hotkey)
		# Update hotkey in gconf
		gconf_client = gconf.client_get_default()
		gconf_client.set_string(FAN_GCONF_KEY_RUN, hotkey)
	
	def SetWebcam(self, hotkey):
		self.webcam = hotkey
		config.setWebcamHotkey(hotkey)
		# Update hotkey in gconf
		gconf_client = gconf.client_get_default()
		gconf_client.set_string(WEBCAM_GCONF_KEY_RUN, hotkey)
	
	def SetWireless(self, hotkey):
		self.wireless = hotkey
		config.setWirelessHotkey(hotkey)
		# Update hotkey in gconf
		gconf_client = gconf.client_get_default()
		gconf_client.set_string(WIRELESS_GCONF_KEY_RUN, hotkey)
