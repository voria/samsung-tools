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
BACKLIGHT_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "8"
BLUETOOTH_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "9"
FAN_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "10"
WEBCAM_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "11"
WIRELESS_GCONF_KEY_COMMAND = GCONF_KEY_COMMAND + "12"

GCONF_KEY_RUN = "/apps/metacity/global_keybindings/run_command_"
BACKLIGHT_GCONF_KEY_RUN = GCONF_KEY_RUN + "8"
BLUETOOTH_GCONF_KEY_RUN = GCONF_KEY_RUN + "9"
FAN_GCONF_KEY_RUN = GCONF_KEY_RUN + "10"
WEBCAM_GCONF_KEY_RUN = GCONF_KEY_RUN + "11"
WIRELESS_GCONF_KEY_RUN = GCONF_KEY_RUN + "12"

BACKLIGHT_COMMAND = "samsung-tools -b toggle --show-notify"
BLUETOOTH_COMMAND = "samsung-tools -B toggle --show-notify"
FAN_COMMAND = "samsung-tools -f hotkey --show-notify"
WEBCAM_COMMAND = "samsung-tools -w toggle --show-notify"
WIRELESS_COMMAND = "samsung-tools -W toggle --show-notify"

class Hotkeys(dbus.service.Object):
	""" Control hotkeys """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.config = SessionConfig(USER_CONFIG_FILE)
		self.backlight = self.config.getBacklightHotkey()
		self.bluetooth = self.config.getBluetoothHotkey()
		self.fan = self.config.getFanHotkey()
		self.webcam = self.config.getWebcamHotkey()
		self.wireless = self.config.getWirelessHotkey()
		## Set hotkeys in gconf
		gconf_client = gconf.client_get_default()
		if self.backlight != "none":
			gconf_client.set_string(BACKLIGHT_GCONF_KEY_COMMAND, BACKLIGHT_COMMAND)
			gconf_client.set_string(BACKLIGHT_GCONF_KEY_RUN, self.backlight)
		else:
			if gconf_client.get_string(BACKLIGHT_GCONF_KEY_COMMAND) == BACKLIGHT_COMMAND:
				gconf_client.unset(BACKLIGHT_GCONF_KEY_COMMAND)
				gconf_client.unset(BACKLIGHT_GCONF_KEY_RUN)
		if self.bluetooth != "none":
			gconf_client.set_string(BLUETOOTH_GCONF_KEY_COMMAND, BLUETOOTH_COMMAND)
			gconf_client.set_string(BLUETOOTH_GCONF_KEY_RUN, self.bluetooth)
		else:
			if gconf_client.get_string(BLUETOOTH_GCONF_KEY_COMMAND) == BLUETOOTH_COMMAND:
				gconf_client.unset(BLUETOOTH_GCONF_KEY_COMMAND)
				gconf_client.unset(BLUETOOTH_GCONF_KEY_RUN)
		if self.fan != "none":
			gconf_client.set_string(FAN_GCONF_KEY_COMMAND, FAN_COMMAND)
			gconf_client.set_string(FAN_GCONF_KEY_RUN, self.fan)
		else:
			if gconf_client.get_string(FAN_GCONF_KEY_COMMAND) == FAN_COMMAND:
				gconf_client.unset(FAN_GCONF_KEY_COMMAND)
				gconf_client.unset(FAN_GCONF_KEY_RUN)
		if self.webcam != "none":
			gconf_client.set_string(WEBCAM_GCONF_KEY_COMMAND, WEBCAM_COMMAND)
			gconf_client.set_string(WEBCAM_GCONF_KEY_RUN, self.webcam)
		else:
			if gconf_client.get_string(WEBCAM_GCONF_KEY_COMMAND) == WEBCAM_COMMAND:
				gconf_client.unset(WEBCAM_GCONF_KEY_COMMAND)
				gconf_client.unset(WEBCAM_GCONF_KEY_RUN)
		if self.wireless != "none":
			gconf_client.set_string(WIRELESS_GCONF_KEY_COMMAND, WIRELESS_COMMAND)
			gconf_client.set_string(WIRELESS_GCONF_KEY_RUN, self.wireless)
		else:
			if gconf_client.get_string(WIRELESS_GCONF_KEY_COMMAND) == WIRELESS_COMMAND:
				gconf_client.unset(WIRELESS_GCONF_KEY_COMMAND)
				gconf_client.unset(WIRELESS_GCONF_KEY_RUN)
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetBacklightHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for backlight control. """
		return self.backlight
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetBluetoothHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for bluetooth control. """
		return self.bluetooth
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetFanHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for fan control. """
		return self.fan
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWebcamHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for webcam control. """
		return self.webcam
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetWirelessHotkey(self, sender = None, conn = None):
		""" Return the current hotkey for wireless control. """
		return self.wireless 
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetBacklightHotkey(self, hotkey, sender = None, conn = None):
		""" Set the hotkey for backlight control. """
		""" If hotkey == "none" (as a string), hotkey will be disabled. """
		gconf_client = gconf.client_get_default()
		if hotkey != "none":
			gconf_client.set_string(BACKLIGHT_GCONF_KEY_COMMAND, BACKLIGHT_COMMAND)
			gconf_client.set_string(BACKLIGHT_GCONF_KEY_RUN, hotkey)
		else:
			gconf_client.unset(BACKLIGHT_GCONF_KEY_RUN)
			gconf_client.unset(BACKLIGHT_GCONF_KEY_COMMAND)
		self.backlight = hotkey
		self.config.setBacklightHotkey(hotkey)		

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetBluetoothHotkey(self, hotkey, sender = None, conn = None):
		""" Set the hotkey for bluetooth control. """
		""" If hotkey == "none" (as a string), hotkey will be disabled. """
		gconf_client = gconf.client_get_default()
		if hotkey != "none":
			gconf_client.set_string(BLUETOOTH_GCONF_KEY_COMMAND, BLUETOOTH_COMMAND)
			gconf_client.set_string(BLUETOOTH_GCONF_KEY_RUN, hotkey)
		else:
			gconf_client.unset(BLUETOOTH_GCONF_KEY_RUN)
			gconf_client.unset(BLUETOOTH_GCONF_KEY_COMMAND)
		self.bluetooth = hotkey
		self.config.setBluetoothHotkey(hotkey)

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanHotkey(self, hotkey, sender = None, conn = None):
		""" Set the hotkey for CPU fan control. """
		""" If hotkey == "none" (as a string), hotkey will be disabled. """
		gconf_client = gconf.client_get_default()
		if hotkey != "none":
			gconf_client.set_string(FAN_GCONF_KEY_COMMAND, FAN_COMMAND)
			gconf_client.set_string(FAN_GCONF_KEY_RUN, hotkey)
		else:
			gconf_client.unset(FAN_GCONF_KEY_RUN)
			gconf_client.unset(FAN_GCONF_KEY_COMMAND)
		self.fan = hotkey
		self.config.setFanHotkey(hotkey)

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWebcamHotkey(self, hotkey, sender = None, conn = None):
		""" Set the hotkey for webcam control. """
		""" If hotkey == "none" (as a string), hotkey will be disabled. """
		gconf_client = gconf.client_get_default()
		if hotkey != "none":
			gconf_client.set_string(WEBCAM_GCONF_KEY_COMMAND, WEBCAM_COMMAND)
			gconf_client.set_string(WEBCAM_GCONF_KEY_RUN, hotkey)
		else:
			gconf_client.unset(WEBCAM_GCONF_KEY_RUN)
			gconf_client.unset(WEBCAM_GCONF_KEY_COMMAND)
		self.webcam = hotkey
		self.config.setWebcamHotkey(hotkey)
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 's', out_signature = None,
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetWirelessHotkey(self, hotkey, sender = None, conn = None):
		""" Set the hotkey for wireless control. """
		""" If hotkey == "none" (as a string), hotkey will be disabled. """
		gconf_client = gconf.client_get_default()
		if hotkey != "none":
			gconf_client.set_string(WIRELESS_GCONF_KEY_COMMAND, WIRELESS_COMMAND)
			gconf_client.set_string(WIRELESS_GCONF_KEY_RUN, hotkey)
		else:
			gconf_client.unset(WIRELESS_GCONF_KEY_RUN)
			gconf_client.unset(WIRELESS_GCONF_KEY_COMMAND)
		self.wireless = hotkey
		self.config.setWirelessHotkey(hotkey)
