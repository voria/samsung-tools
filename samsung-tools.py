#!/usr/bin/python2
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
import sys
WORK_DIRECTORY = "/usr/lib/samsung-tools"
sys.path.append(WORK_DIRECTORY)

from optparse import OptionParser
import dbus

import gettext
_ = gettext.gettext
gettext.bindtextdomain("samsung-tools")
gettext.textdomain("samsung-tools")

from backends.globals import *
from backends.session.util.locales import *

quiet = False

class Backlight():
	def __init__(self, option):
		self.option = option
		success = False
		retry = 3
		while retry > 0 and success == False:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_BACKLIGHT)
				self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
				success = True
			except:
				retry = retry - 1
		if retry == 0:
			print unicode(_("Backlight control: unable to connect to session service!"), "utf-8")
			sys.exit(1)

	def __on(self):
		return self.interface.Enable()

	def __off(self):
		return self.interface.Disable()

	def __status(self):
		return self.interface.IsEnabled()

	def __toggle(self):
		return self.interface.Toggle()

	def apply(self):
		if self.option == None:
			return
		if self.option == "on":
			result = self.__on()
			if not quiet:
				if result == True:
					print BACKLIGHT_ENABLED
				else:
					print BACKLIGHT_ENABLING_ERROR
		if self.option == "off":
			result = self.__off()
			if not quiet:
				if result == True:
					print BACKLIGHT_DISABLED
				else:
					print BACKLIGHT_DISABLING_ERROR
		if self.option == "toggle":
			result = self.__toggle()
			if not quiet:
				if result == True:
					status = self.__status()
					if status == True:
						print BACKLIGHT_ENABLED
					else:
						print BACKLIGHT_DISABLED
				else:
					print BACKLIGHT_TOGGLING_ERROR
		if self.option == "hotkey":
			from time import sleep
			from subprocess import Popen, PIPE
			tempfiles = ".samsung-tools-backlight-" + str(os.getuid()) + "-"
			tempfile = "/tmp/" + tempfiles + str(os.getpid())
			toggle = True
			try:
				ls = Popen(['ls /tmp/' + tempfiles + '*'], stdout = PIPE, stderr = PIPE, shell = True)
				if len(ls.communicate()[0]) != 0:
					toggle = False
			except:
				pass
			if toggle == True:
				Backlight("toggle").apply()
				try:
					file = open(tempfile, "w").close() # create temp file
				except:
					pass
				sleep(0.5)
				try:
					os.remove(tempfile)
				except:
					pass
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == True:
					print BACKLIGHT_STATUS_ENABLED
				else:
					print BACKLIGHT_STATUS_DISABLED

class Bluetooth():
	def __init__(self, option, use_notify = False):
		self.option = option
		self.use_notify = use_notify
		success = False
		retry = 3
		while retry > 0 and success == False:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_BLUETOOTH)
				self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
				success = True
			except:
				retry = retry - 1
		if retry == 0:
			print unicode(_("Bluetooth control: unable to connect to session service!"), "utf-8")
			sys.exit(1)

	def __is_available(self):
		return self.interface.IsAvailable()

	def __on(self):
		return self.interface.Enable(self.use_notify)

	def __off(self):
		return self.interface.Disable(self.use_notify)

	def __toggle(self):
		return self.interface.Toggle(self.use_notify)

	def __status(self):
		return self.interface.IsEnabled(self.use_notify)

	def apply(self):
		if self.option == None:
			return
		if not self.__is_available():
			if not quiet:
				print BLUETOOTH_NOT_AVAILABLE
			self.__status() # needed to show notification
			return
		if self.option == "on":
			result = self.__on()
			if not quiet:
				if result == True:
					print BLUETOOTH_ENABLED
				else:
					print BLUETOOTH_ENABLING_ERROR
		if self.option == "off":
			result = self.__off()
			if not quiet:
				if result == True:
					print BLUETOOTH_DISABLED
				else:
					print BLUETOOTH_DISABLING_ERROR
		if self.option == "toggle":
			result = self.__toggle()
			if not quiet:
				if result == True:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					status = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if status == True:
						print BLUETOOTH_ENABLED
					else:
						print BLUETOOTH_DISABLED
				else:
					print BLUETOOTH_TOGGLING_ERROR
		if self.option == "hotkey":
			from time import sleep
			from subprocess import Popen, PIPE
			tempfiles = ".samsung-tools-bluetooth-" + str(os.getuid()) + "-"
			tempfile = "/tmp/" + tempfiles + str(os.getpid())
			toggle = True
			try:
				ls = Popen(['ls /tmp/' + tempfiles + '*'], stdout = PIPE, stderr = PIPE, shell = True)
				if len(ls.communicate()[0]) != 0:
					toggle = False
			except:
				pass
			if toggle == True:
				Bluetooth("toggle", self.use_notify).apply()
				try:
					file = open(tempfile, "w").close() # create temp file
				except:
					pass
				sleep(0.5)
				try:
					os.remove(tempfile)
				except:
					pass
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == True:
					print BLUETOOTH_STATUS_ENABLED
				else:
					print BLUETOOTH_STATUS_DISABLED

class Cpu():
	def __init__(self, option, use_notify = False):
		self.option = option
		self.use_notify = use_notify
		success = False
		retry = 3
		while retry > 0 and success == False:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_CPU)
				self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
				success = True
			except:
				retry = retry - 1
		if retry == 0:
			print unicode(_("CPU fan control: unable to connect to session service!"), "utf-8")
			sys.exit(1)

	def __is_temperature_available(self):
		return self.interface.IsTemperatureAvailable()

	def __is_fan_available(self):
		return self.interface.IsFanAvailable()

	def __temp(self):
		return self.interface.GetTemperature()

	def __normal(self):
		return self.interface.SetFanNormal(self.use_notify)

	def __silent(self):
		return self.interface.SetFanSilent(self.use_notify)

	def __overclock(self):
		return self.interface.SetFanOverclock(self.use_notify)

	def __cycle(self):
		return self.interface.Cycle(self.use_notify)

	def __status(self):
		return self.interface.Status(self.use_notify)

	def apply(self):
		if self.option == None:
			return
		if self.__is_temperature_available() and self.option != "hotkey" and not quiet:
			print CPU_TEMPERATURE + " " + self.__temp() + unicode(" °C", "utf8")
		if not self.__is_fan_available():
			if not quiet:
				print FAN_NOT_AVAILABLE
			self.__status() # needed to show notification
			return
		if self.option == "normal":
			result = self.__normal()
			if not quiet:
				if result == True:
					print FAN_STATUS_NORMAL
				else:
					print FAN_SWITCHING_ERROR
		if self.option == "silent":
			result = self.__silent()
			if not quiet:
				if result == True:
					print FAN_STATUS_SILENT
				else:
					print FAN_SWITCHING_ERROR
		if self.option == "overclock":
			result = self.__overclock()
			if not quiet:
				if result == True:
					print FAN_STATUS_OVERCLOCK
				else:
					print FAN_SWITCHING_ERROR
		if self.option == "cycle":
			result = self.__cycle()
			if not quiet:
				if result == True:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					mode = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if mode == 0:
						print FAN_STATUS_NORMAL
					if mode == 1:
						print FAN_STATUS_SILENT
					if mode == 2:
						print FAN_STATUS_OVERCLOCK
					if mode == 3:
						print FAN_STATUS_ERROR
				else:
					print FAN_SWITCHING_ERROR
		if self.option == "hotkey":
			from time import sleep
			from subprocess import Popen, PIPE
			tempfiles = ".samsung-tools-cpu-" + str(os.getuid()) + "-"
			tempfile = "/tmp/" + tempfiles + str(os.getpid())
			hotkey = True
			try:
				ls = Popen(['ls /tmp/' + tempfiles + '*'], stdout = PIPE, stderr = PIPE, shell = True)
				if len(ls.communicate()[0]) != 0:
					hotkey = False
			except:
				pass
			if hotkey == True:
				Cpu("hotkey2", self.use_notify).apply()
				try:
					file = open(tempfile, "w").close() # create temp file
				except:
					pass
				sleep(0.5)
				try:
					os.remove(tempfile)
				except:
					pass
		if self.option == "hotkey2":
			from time import sleep
			from subprocess import Popen, PIPE
			tempfiles = ".samsung-tools-cpufan-" + str(os.getuid()) + "-"
			tempfile = "/tmp/" + tempfiles + str(os.getpid())
			action = "status"
			try:
				ls = Popen(['ls /tmp/' + tempfiles + '*'], stdout = PIPE, stderr = PIPE, shell = True)
				if len(ls.communicate()[0]) != 0:
					action = "cycle"
			except:
				pass
			Cpu(action, self.use_notify).apply()
			try:
				file = open(tempfile, "w").close() # create temp file
			except:
				pass
			sleep(9.5)
			try:
				os.remove(tempfile)
			except:
				pass
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == 0:
					print FAN_STATUS_NORMAL
				if result == 1:
					print FAN_STATUS_SILENT
				if result == 2:
					print FAN_STATUS_OVERCLOCK
				if result == 3:
					print FAN_STATUS_ERROR

class Webcam():
	def __init__(self, option, use_notify = False):
		self.option = option
		self.use_notify = use_notify
		success = False
		retry = 3
		while retry > 0 and success == False:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_WEBCAM)
				self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
				success = True
			except:
				retry = retry - 1
		if retry == 0:
			print unicode(_("Webcam control: unable to connect to session service!"), "utf-8")
			sys.exit(1)

	def __is_available(self):
		return self.interface.IsAvailable()

	def __on(self):
		return self.interface.Enable(self.use_notify)

	def __off(self):
		return self.interface.Disable(self.use_notify)

	def __toggle(self):
		return self.interface.Toggle(self.use_notify)

	def __status(self):
		return self.interface.IsEnabled(self.use_notify)

	def apply(self):
		if self.option == None:
			return
		if not self.__is_available():
			if not quiet:
				print WEBCAM_NOT_AVAILABLE
			self.__status() # needed to show notification
			return
		if self.option == "on":
			result = self.__on()
			if not quiet:
				if result == True:
					print WEBCAM_ENABLED
				else:
					print WEBCAM_ENABLING_ERROR
		if self.option == "off":
			result = self.__off()
			if not quiet:
				if result == True:
					print WEBCAM_DISABLED
				else:
					print WEBCAM_DISABLING_ERROR
		if self.option == "toggle":
			result = self.__toggle()
			if not quiet:
				if result == True:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					status = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if status == True:
						print WEBCAM_ENABLED
					else:
						print WEBCAM_DISABLED
				else:
					print WEBCAM_TOGGLING_ERROR
		if self.option == "hotkey":
			from time import sleep
			from subprocess import Popen, PIPE
			tempfiles = ".samsung-tools-webcam-" + str(os.getuid()) + "-"
			tempfile = "/tmp/" + tempfiles + str(os.getpid())
			toggle = True
			try:
				ls = Popen(['ls /tmp/' + tempfiles + '*'], stdout = PIPE, stderr = PIPE, shell = True)
				if len(ls.communicate()[0]) != 0:
					toggle = False
			except:
				pass
			if toggle == True:
				Webcam("toggle", self.use_notify).apply()
				try:
					file = open(tempfile, "w").close() # create temp file
				except:
					pass
				sleep(0.5)
				try:
					os.remove(tempfile)
				except:
					pass
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == True:
					print WEBCAM_STATUS_ENABLED
				else:
					print WEBCAM_STATUS_DISABLED

class Wireless():
	def __init__(self, option, use_notify = False):
		self.option = option
		self.use_notify = use_notify
		success = False
		retry = 3
		while retry > 0 and success == False:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_WIRELESS)
				self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
				success = True
			except:
				retry = retry - 1
		if retry == 0:
			print unicode(_("Wireless control: unable to connect to session service!"), "utf-8")
			sys.exit(1)

	def __is_available(self):
		return self.interface.IsAvailable()

	def __on(self):
		return self.interface.Enable(self.use_notify)

	def __off(self):
		return self.interface.Disable(self.use_notify)

	def __toggle(self):
		return self.interface.Toggle(self.use_notify)

	def __status(self):
		return self.interface.IsEnabled(self.use_notify)

	def apply(self):
		if self.option == None:
			return
		if not self.__is_available():
			if not quiet:
				print WIRELESS_NOT_AVAILABLE
			self.__status() # needed to show notification
			return
		if self.option == "on":
			result = self.__on()
			if not quiet:
				if result == True:
					print WIRELESS_ENABLED
				else:
					print WIRELESS_ENABLING_ERROR
		if self.option == "off":
			result = self.__off()
			if not quiet:
				if result == True:
					print WIRELESS_DISABLED
				else:
					print WIRELESS_DISABLING_ERROR
		if self.option == "toggle":
			result = self.__toggle()
			if not quiet:
				if result == True:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					status = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if status == True:
						print WIRELESS_ENABLED
					else:
						print WIRELESS_DISABLED
				else:
					print WIRELESS_TOGGLING_ERROR
		if self.option == "hotkey":
			from time import sleep
			from subprocess import Popen, PIPE
			tempfiles = ".samsung-tools-wireless-" + str(os.getuid()) + "-"
			tempfile = "/tmp/" + tempfiles + str(os.getpid())
			toggle = True
			try:
				ls = Popen(['ls /tmp/' + tempfiles + '*'], stdout = PIPE, stderr = PIPE, shell = True)
				if len(ls.communicate()[0]) != 0:
					toggle = False
			except:
				pass
			if toggle == True:
				Wireless("toggle", self.use_notify).apply()
				try:
					file = open(tempfile, "w").close() # create temp file
				except:
					pass
				sleep(0.5)
				try:
					os.remove(tempfile)
				except:
					pass
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == True:
					print WIRELESS_STATUS_ENABLED
				else:
					print WIRELESS_STATUS_DISABLED

def usage(option = None, opt = None, value = None, parser = None):
	print "Samsung Tools", APP_VERSION, "-",
	print unicode(_("Command Line Utility"), "utf-8")
	print
	print unicode(_("Usage: %s <interface> <option> ...") % os.path.basename(sys.argv[0]), "utf-8")
	print
	print unicode(_("Backlight:"), "utf-8")
	print "\t" + unicode(_("Interface"), "utf-8") + ":\t-b | --backlight"
	print "\t" + unicode(_("Options"), "utf-8") + ":\ton | off | toggle | hotkey | status"
	print unicode(_("Bluetooth:"), "utf-8")
	print "\t" + unicode(_("Interface"), "utf-8") + ":\t-B | --bluetooth"
	print "\t" + unicode(_("Options"), "utf-8") + ":\ton | off | toggle | hotkey | status"
	print unicode(_("CPU fan:"), "utf-8")
	print "\t" + unicode(_("Interface"), "utf-8") + ":\t-c | --cpu"
	print "\t" + unicode(_("Options"), "utf-8") + ":\tnormal | silent | overclock | cycle | hotkey | status"
	print unicode(_("Webcam:"), "utf-8")
	print "\t" + unicode(_("Interface"), "utf-8") + ":\t-w | --webcam"
	print "\t" + unicode(_("Options"), "utf-8") + ":\ton | off | toggle | hotkey | status"
	print unicode(_("Wireless:"), "utf-8")
	print "\t" + unicode(_("Interface"), "utf-8") + ":\t-W | --wireless"
	print "\t" + unicode(_("Options"), "utf-8") + ":\ton | off | toggle | hotkey | status"
	print
	print unicode(_("Other options:"), "utf-8")
	print " -a | --status\t\t" + unicode(_("Show status for all devices."), "utf-8")
	print " -n | --show-notify\t" + unicode(_("Show graphical notifications."), "utf-8")
	print " -q | --quiet\t\t" + unicode(_("Do not print messages on standard output."), "utf-8")
	print " -i | --interface\t" + unicode(_("Show the control interface currently in use."), "utf-8")
	print " -s | --stop-session\t" + unicode(_("Stop the session service."), "utf-8")
	print " -S | --stop-system\t" + unicode(_("Stop the system service."), "utf-8")
	print
	print unicode(_("Examples of use:"), "utf-8")
	print unicode(_(" - Toggle backlight:"), "utf-8")
	print " %s --backlight toggle" % os.path.basename(sys.argv[0])
	print
	print unicode(_(" - Toggle wireless and set CPU fan mode to 'silent':"), "utf-8")
	print " %s --wireless toggle --cpu silent" % os.path.basename(sys.argv[0])
	print
	print unicode(_(" - Disable bluetooth, webcam and wireless:"), "utf-8")
	print " %s -B off -w off -W off" % os.path.basename(sys.argv[0])
	print
	print unicode(_("For more informations, visit the 'Linux On My Samsung' forum:"), "utf-8")
	print
	print " - http://www.voria.org/forum"
	print
	print "Copyleft by: Fortunato Ventre (voRia) - vorione@gmail.com"
	print unicode(_("Released under GPLv3 license"), "utf-8") + "."
	sys.exit(0)

def main():
	if  len(sys.argv) == 1:
		print unicode(_("No action(s) specified."), "utf-8")
		print unicode(_("Use --help for instructions."), "utf-8")
		sys.exit(1)

	usage_string = unicode(_("Usage: %s <interface> <option> ...") % os.path.basename(sys.argv[0]), "utf-8")
	parser = OptionParser(usage_string, add_help_option = False)
	parser.add_option('-h', '--help',
					action = "callback",
					callback = usage)
	parser.add_option('-b', '--backlight',
					dest = "backlight",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'hotkey', 'status'])
	parser.add_option('-B', '--bluetooth',
					dest = "bluetooth",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'hotkey', 'status'])
	parser.add_option('-c', '--cpu',
					dest = "cpu",
					type = "choice",
					choices = ['normal', 'silent', 'overclock', 'cycle', 'hotkey', 'status'])
	parser.add_option('-w', '--webcam',
					dest = "webcam",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'hotkey', 'status'])
	parser.add_option('-W', '--wireless',
					dest = "wireless",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'hotkey', 'status'])
	parser.add_option('-n', '--show-notify',
					action = "store_true",
					dest = "show_notify",
					default = False)
	parser.add_option('-q', '--quiet',
					action = "store_true",
					dest = "quiet",
					default = False)
	parser.add_option('-i', '--interface',
					action = "store_true",
					dest = "interface",
					default = False)
	parser.add_option('-s', '--stop-session',
					action = "store_true",
					dest = "stopsession",
					default = False)
	parser.add_option('-S', '--stop-system',
					action = "store_true",
					dest = "stopsystem",
					default = False)
	parser.add_option('-a', '--status',
					action = "store_true",
					dest = "status",
					default = False)

	(options, args) = parser.parse_args()

	global quiet
	quiet = options.quiet

	if options.status == True:
		options.backlight = "status"
		options.bluetooth = "status"
		options.cpu = "status"
		options.webcam = "status"
		options.wireless = "status"

	if os.getuid() == 0:
		print unicode(_("This program is intended to be used only by non-privileged users."), "utf-8")
		sys.exit(1)

	if len(args) != 0:
		print unicode(_("Wrong argument(s)."), "utf-8")
		print unicode(_("Use --help for instructions."), "utf-8")
		sys.exit(1)

	# Check if the dbus daemon is running. If not, start it.
	if "DBUS_SESSION_BUS_ADDRESS" not in os.environ:
		try:
			from subprocess import Popen, PIPE, STDOUT
			p = Popen('dbus-launch --exit-with-session', shell = True, stdout = PIPE, stderr = STDOUT)
			for var in p.stdout:
				sp = var.split('=', 1)
				os.environ[sp[0]] = sp[1][:-1]
		except:
			print unicode(_("Unable to start a DBus daemon!"), "utf-8")
			sys.exit(1)

	Backlight(options.backlight).apply()
	Bluetooth(options.bluetooth, options.show_notify).apply()
	Cpu(options.cpu, options.show_notify).apply()
	Webcam(options.webcam, options.show_notify).apply()
	Wireless(options.wireless, options.show_notify).apply()

	if options.interface == True and not quiet:
		try:
			bus = dbus.SystemBus()
			proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_OPTIONS)
			opts = dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			ci = opts.GetControlInterface()
			print unicode(_("Control interface:"), "utf-8"),
			if ci == "esdm":
				print "easy-slow-down-manager"
			elif ci == "sl":
				print "samsung-laptop"
			else:
				print "-"
		except:
			print unicode(_("Control interface: unable to connect to system service!"), "utf-8")
			pass

	if options.stopsession == True:
		try:
			bus = dbus.SessionBus()
			proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_GENERAL)
			general = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
			general.Exit()
			if not quiet:
				print unicode(_("Session service stopped"), "utf-8")
		except:
			if not quiet:
				print unicode(_("Cannot stop session service"), "utf-8")
			pass

	if options.stopsystem == True:
		try:
			bus = dbus.SystemBus()
			proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_GENERAL)
			general = dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			general.Exit()
			if not quiet:
				print unicode(_("System service stopped"), "utf-8")
		except:
			if not quiet:
				print unicode(_("Cannot stop system service"), "utf-8")
			pass

if __name__ == "__main__":
	main()
