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

from backends.log import Log

APP_NAME = "Samsung Tools"
APP_VERSION = "2.1"
WORK_DIRECTORY = "/usr/share/samsung-tools/"

AUTHORS_LIST = [ "Fortunato Ventre" ]
ARTISTS_LIST = [ "http://icons.mysitemyway.com" ]
TRANSLATORS_LIST = [
					"Fortunato Ventre",
					"Lionel BASTET",
					"miplou",
					"sk",
					"Jonathan Cragg",
					"nanker",
					"mysza-j",
					"papukaija",
					"ironfisher",
					"joel morren",
					"subiraj",
					"Jonay",
					"zeugma",
					"Joshua Schroijen",
					"Sukochev Roman (Leolik)",
					"Andrey Kulakov",
					"Dr. Alex Arutyunjan",
					"Cezary Jackiewicz",
					"Lars Karlsson",
					"Krasznecz Zoltán",
					"Sergiy Gavrylov",
					"Dirk Roos",
					"Michael Likholet",
					"Kristian Gomes",
					"Bruno Veilleux",
					"zzz",
					"Inox",
					"Thibault Févry",
					"Fitoschido",
					"Adriano Steffler",
					"taha",
					"Piotr Sokół",
					"Мирослав Николић",
					"Giordano Bruno Barbosa",
					"Benedict Etzel",
					"Aiguanachein",
					"simon",
					"D3NMOH",
					"Felipe Amaral",
					"Baptiste Fontaine",
					"Daniel Manrique",
					"Stanislas Michalak",
					"Виталий",
					"SweX",
					"František Zatloukal",
					"abuyop",
					"Hubert \"Schlussarz\" Ślósarski",
					"Rafael Neri",
					"André Drumond",
					"Antoine Tonio",
					"naitong",
					"Dennis Baudys",
					"Sascha Biermanns",
					"Novikov Andrey",
					"Juan Pablo",
					"Praveen Illa",
					"Adolfo Jayme Barrientos",
					"Kim Boram",
					"Volkan Gezer",
					"Maurício Meneghini Fauth"
					]

# Interface/Objects for session service
SESSION_INTERFACE_NAME = "org.voria.SamsungTools.Session"
SESSION_OBJECT_PATH_GENERAL = "/"
SESSION_OBJECT_PATH_OPTIONS = "/Options"
SESSION_OBJECT_PATH_BACKLIGHT = "/Device/Backlight"
SESSION_OBJECT_PATH_BLUETOOTH = "/Device/Bluetooth"
SESSION_OBJECT_PATH_CPU = "/Device/Cpu"
SESSION_OBJECT_PATH_WEBCAM = "/Device/Webcam"
SESSION_OBJECT_PATH_WIRELESS = "/Device/Wireless"
# Interface/Objects for system service
SYSTEM_INTERFACE_NAME = "org.voria.SamsungTools.System"
SYSTEM_OBJECT_PATH_GENERAL = "/"
SYSTEM_OBJECT_PATH_OPTIONS = "/Options"
SYSTEM_OBJECT_PATH_LAPTOPMODE = "/Options/LaptopMode"
SYSTEM_OBJECT_PATH_SYSCTL = "/Options/SysCtl"
SYSTEM_OBJECT_PATH_POWERMANAGEMENT = "/Options/PowerManagement"
SYSTEM_OBJECT_PATH_BACKLIGHT = "/Device/Backlight"
SYSTEM_OBJECT_PATH_BLUETOOTH = "/Device/Bluetooth"
SYSTEM_OBJECT_PATH_CPU = "/Device/Cpu"
SYSTEM_OBJECT_PATH_FAN = "/Device/Fan"
SYSTEM_OBJECT_PATH_WEBCAM = "/Device/Webcam"
SYSTEM_OBJECT_PATH_WIRELESS = "/Device/Wireless"

# Power management scripts locations
PM_DEVICES_POWER_MANAGEMENT = "/usr/lib/pm-utils/power.d/samsung-tools_devices-power-management"
PM_USB_AUTOSUSPEND = "/usr/lib/pm-utils/power.d/samsung-tools_usb-autosuspend"
PM_VM_WRITEBACK_TIME = "/usr/lib/pm-utils/power.d/samsung-tools_vm-writeback-time"

import sys, os.path
###
### Stuff for session service only
###
if os.path.basename(sys.argv[0]) == "session-service.py":
	# Config/Log
	SESSION_CONFIG_FILE = "/etc/samsung-tools/session.conf"
	USER_DIRECTORY = os.path.join(os.getenv('HOME'), ".samsung-tools")
	USER_CONFIG_FILE = os.path.join(USER_DIRECTORY, os.path.basename(SESSION_CONFIG_FILE))
	SESSION_LOG_FILE = os.path.join(USER_DIRECTORY, "log")
	sessionlog = Log(SESSION_LOG_FILE)
	from backends.session.util.config import SessionConfig
	sessionconfig = SessionConfig(USER_CONFIG_FILE)

###
### Stuff for system service only
###
if os.path.basename(sys.argv[0]) == "system-service.py":
	# Config/Log
	SYSTEM_CONFIG_FILE = "/etc/samsung-tools/system.conf"
	SYSTEM_LOG_FILE = "/var/log/samsung-tools.log"
	systemlog = Log(SYSTEM_LOG_FILE)
	from backends.system.util.config import SystemConfig
	systemconfig = SystemConfig(SYSTEM_CONFIG_FILE)
	# Control interface
	CONTROL_INTERFACE = os.path.join(WORK_DIRECTORY, "control_interface")
	# Last devices' status files
	LAST_DEVICES_STATUS_DIRECTORY = os.path.join(WORK_DIRECTORY, "devices-status")
	LAST_DEVICE_STATUS_BACKLIGHT = os.path.join(LAST_DEVICES_STATUS_DIRECTORY, "backlight")
	LAST_DEVICE_STATUS_BLUETOOTH = os.path.join(LAST_DEVICES_STATUS_DIRECTORY, "bluetooth")
	LAST_DEVICE_STATUS_WEBCAM = os.path.join(LAST_DEVICES_STATUS_DIRECTORY, "webcam")
	LAST_DEVICE_STATUS_WIRELESS = os.path.join(LAST_DEVICES_STATUS_DIRECTORY, "wireless")
	LAST_DEVICE_STATUS_CPUFAN = os.path.join(LAST_DEVICES_STATUS_DIRECTORY, "cpufan")
	# system service does not have a PATH specified, so we will specify one manually.
	os.environ['PATH'] = "/sbin:/usr/sbin:/bin:/usr/bin"
	# Commands
	COMMAND_MODPROBE = "modprobe"
	COMMAND_VBETOOL = "vbetool"
	COMMAND_LSMOD = "lsmod"
	COMMAND_DMESG = "dmesg"
	COMMAND_RFKILL = "rfkill"
	COMMAND_SYSCTL = "sysctl"
	# Scripts
	SCRIPT_BLUETOOTH_ON = "/etc/samsung-tools/scripts/bluetooth-on"
	SCRIPT_BLUETOOTH_OFF = "/etc/samsung-tools/scripts/bluetooth-off"
	SCRIPT_WIRELESS_ON = "/etc/samsung-tools/scripts/wireless-on"
	SCRIPT_WIRELESS_OFF = "/etc/samsung-tools/scripts/wireless-off"
	# easy-slow-down-manager interface
	ESDM_MODULE = "easy_slow_down_manager"
	ESDM_PATH_BACKLIGHT = "/proc/easy_backlight"
	ESDM_PATH_PERFORMANCE = "/proc/easy_slow_down_manager"
	ESDM_PATH_WIRELESS = "/proc/easy_wifi_kill"
	# samsung-laptop interface
	SL_MODULE = "samsung-laptop"
	SL_PATH_BACKLIGHT = "/sys/devices/platform/samsung/backlight/samsung/bl_power"
	SL_PATH_PERFORMANCE = "/sys/devices/platform/samsung/performance_level"
	# Temperature
	CPU_TEMPERATURE_PATH = "/sys/class/thermal/thermal_zone0/temp"
	# sysctl configuration file
	SYSCTL_CONFIG_FILE = "/etc/sysctl.conf"
