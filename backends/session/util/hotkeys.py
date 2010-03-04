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

from backends.globals import *

try:
	import gconf
except:
	log_session.write("ERROR: 'hotkeys'  - cannot import gconf.")
	pass

import dbus.service

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
		try:
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
		except:
			log_session.write("ERROR: 'Hotkeys()'  - cannot set hotkeys in gconf.")
			pass
		
	
