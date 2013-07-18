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

from backends.globals import WORK_DIRECTORY

SAMSUNG_TOOLS_ICON = WORK_DIRECTORY + "gui/icons/samsung-tools.png"

FAN_NORMAL_ICON = WORK_DIRECTORY + "gui/icons/fan-normal.png"
FAN_SILENT_ICON = WORK_DIRECTORY + "gui/icons/fan-silent.png"
FAN_OVERCLOCK_ICON = WORK_DIRECTORY + "gui/icons/fan-overclock.png"
WEBCAM_ICON = "camera-web"

# If notify-osd icons are not available, use the default ones
from os.path import exists
if exists("/usr/share/notify-osd/icons/"):
	BLUETOOTH_ICON = "bluetooth"
	WIRELESS_ENABLED_ICON = "notification-network-wireless-none"
	WIRELESS_DISABLED_ICON = "notification-network-wireless-disconnected"
	ERROR_ICON = "error"
	STOP_ICON = "stop"
else:
	BLUETOOTH_ICON = WORK_DIRECTORY + "gui/icons/bluetooth.png"
	WIRELESS_ENABLED_ICON = "network-wireless"
	WIRELESS_DISABLED_ICON = "network-wireless"
	ERROR_ICON = "dialog-error"
	STOP_ICON = "process-stop"
