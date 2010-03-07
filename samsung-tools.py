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
			print _("Backlight control: unable to connect to session service!")
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
				if result == 1:
					print BACKLIGHT_ENABLED
				else:
					print BACKLIGHT_ENABLING_ERROR
		if self.option == "off":
			result = self.__off()
			if not quiet:
				if result == 1:
					print BACKLIGHT_DISABLED
				else:
					print BACKLIGHT_DISABLING_ERROR
		if self.option == "toggle":
			result = self.__toggle()
			if not quiet:
				if result == 1:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					status = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if status == 1:
						print BACKLIGHT_ENABLED
					else:
						print BACKLIGHT_DISABLED
				else:
					print BACKLIGHT_TOGGLING_ERROR				
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == 1:
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
			print _("Bluetooth control: unable to connect to session service!")
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
				if result == 1:
					print BLUETOOTH_ENABLED
				else:
					print BLUETOOTH_ENABLING_ERROR
		if self.option == "off":
			result = self.__off()
			if not quiet:
				if result == 1:
					print BLUETOOTH_DISABLED
				else:
					print BLUETOOTH_DISABLING_ERROR
		if self.option == "toggle":
			result = self.__toggle()
			if not quiet:
				if result == 1:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					status = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if status == 1:
						print BLUETOOTH_ENABLED
					else:
						print BLUETOOTH_DISABLED
				else:
					print BLUETOOTH_TOGGLING_ERROR
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == 1:
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
			print _("CPU control: unable to connect to session service!")
			sys.exit(1)
	
	def __is_available(self):
		return self.interface.IsAvailable()
	
	def __normal(self):
		return self.interface.SetNormal(self.use_notify)
	
	def __silent(self):
		return self.interface.SetSilent(self.use_notify)
	
	def __speed(self):
		return self.interface.SetSpeed(self.use_notify)
	
	def __cycle(self):
		return self.interface.Cycle(self.use_notify)
	
	def __status(self):
		return self.interface.Status(self.use_notify)
	
	def apply(self):
		if self.option == None:
			return
		if not self.__is_available():
			if not quiet:
				print CPU_NOT_AVAILABLE
			self.__status() # needed to show notification
			return
		if self.option == "normal":
			result = self.__normal()
			if not quiet:
				if result == 1:
					print CPU_SWITCH_NORMAL
				else:
					print CPU_SWITCHING_ERROR
		if self.option == "silent":
			result = self.__silent()
			if not quiet:
				if result == 1:
					print CPU_SWITCH_SILENT
				else:
					print CPU_SWITCHING_ERROR
		if self.option == "speed":
			result = self.__speed()
			if not quiet:
				if result == 1:
					print CPU_SWITCH_SPEED
				else:
					print CPU_SWITCHING_ERROR
		if self.option == "cycle":
			result = self.__cycle()
			if not quiet:
				if result == 1:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					mode = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if mode == 0:
						print CPU_SWITCH_NORMAL
					if mode == 1:
						print CPU_SWITCH_SILENT
					if mode == 2:
						print CPU_SWITCH_SPEED
					if mode == 3:
						print CPU_STATUS_ERROR
				else:
					print CPU_SWITCHING_ERROR
		if self.option == "hotkey":
			from time import sleep
			from subprocess import Popen, PIPE
			tempfiles = ".samsung-tools_hotkey-tempfile-"
			tempfile = os.path.join(USER_DIRECTORY, tempfiles + str(os.getpid()))
			action = "status"
			try:
				ls = Popen(['ls', '-a', USER_DIRECTORY], stdout = PIPE)
				output = ls.communicate()[0].split()
				for line in output:
					if line[0:len(tempfiles)] == tempfiles:
						action = "cycle"
						break
			except:
				pass
			Cpu(action, self.use_notify).apply()
			try:
				file = open(tempfile, "w").close() # create temp file
			except:
				pass
			sleep(10)
			try:
				os.remove(tempfile)
			except:
				pass
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == 0:
					print CPU_STATUS_NORMAL
				if result == 1:
					print CPU_STATUS_SILENT
				if result == 2:
					print CPU_STATUS_SPEED
				if result == 3:
					print CPU_STATUS_ERROR
		
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
			print _("Webcam control: unable to connect to session service!")
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
				if result == 1:
					print WEBCAM_ENABLED
				else:
					print WEBCAM_ENABLING_ERROR
		if self.option == "off":
			result = self.__off()
			if not quiet:
				if result == 1:
					print WEBCAM_DISABLED
				else:
					print WEBCAM_DISABLING_ERROR
		if self.option == "toggle":
			result = self.__toggle()
			if not quiet:
				if result == 1:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					status = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if status == 1:
						print WEBCAM_ENABLED
					else:
						print WEBCAM_DISABLED
				else:
					print WEBCAM_TOGGLING_ERROR
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == 1:
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
			print _("Wireless control: unable to connect to session service!")
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
				if result == 1:
					print WIRELESS_ENABLED
				else:
					print WIRELESS_ENABLING_ERROR
		if self.option == "off":
			result = self.__off()
			if not quiet:
				if result == 1:
					print WIRELESS_DISABLED
				else:
					print WIRELESS_DISABLING_ERROR
		if self.option == "toggle":
			result = self.__toggle()
			if not quiet:
				if result == 1:
					# Temporary disable notifications
					n = self.use_notify
					self.use_notify = False
					status = self.__status()
					self.use_notify = n
					# Notification re-enabled
					if status == 1:
						print WIRELESS_STATUS_ENABLED
					else:
						print WIRELESS_STATUS_DISABLED
				else:
					print WIRELESS_TOGGLING_ERROR
		if self.option == "status":
			result = self.__status()
			if not quiet:
				if result == 1:
					print WIRELESS_STATUS_ENABLED
				else:
					print WIRELESS_STATUS_DISABLED

def usage(option = None, opt = None, value = None, parser = None):
	print _("Samsung-Tools - Command Line Utility")
	print
	print _("Usage: %s <interface> <option> ...") % os.path.basename(sys.argv[0])
	print
	print _("Backlight:")
	print "\t" + _("Interface") + ":\t-b | --backlight"
	print "\t" + _("Options") + ":\ton | off | toggle | status"
	print _("Bluetooth:")
	print "\t" + _("Interface") + ":\t-B | --bluetooth"
	print "\t" + _("Options") + ":\ton | off | toggle | status"
	print _("CPU:")
	print "\t" + _("Interface") + ":\t-c | --cpu"
	print "\t" + _("Options") + ":\tnormal | silent | speed | cycle | hotkey | status"
	print _("Webcam:")
	print "\t" + _("Interface") + ":\t-w | --webcam"
	print "\t" + _("Options") + ":\ton | off | toggle | status"
	print _("Wireless:")
	print "\t" + _("Interface") + ":\t-W | --wireless"
	print "\t" + _("Options") + ":\ton | off | toggle | status"
	print
	print _("Other options:")
	print " -n | --show-notify\t" + _("Show graphical notifications.")
	print " -q | --quiet\t\t" + _("Do not print messages on standard output.")
	print " -s | --stop-session\t" + _("Stop the session service.")
	print " -S | --stop-system\t" + _("Stop the system service.")
	print
	print _("Examples of use:")
	print _(" - Toggle backlight:")
	print " %s --backlight toggle" % os.path.basename(sys.argv[0])
	print
	print _(" - Toggle wireless and set CPU to silent:")
	print " %s --wireless toggle --cpu silent" % os.path.basename(sys.argv[0])
	print
	print _(" - Disable bluetooth, webcam and wireless:")
	print " %s -B off -w off -W off" % os.path.basename(sys.argv[0])
	print
	print _("For more informations, visit the 'Linux On My Samsung' forum, at:")
	print
	print " - http://www.voria.org/forum"
	print
	print "Copyleft by: Fortunato Ventre (voRia) - vorione@gmail.com"
	print _("Released under GPLv3 license.")
	sys.exit(0)

def main():
	if  len(sys.argv) == 1:
		print _("No action(s) specified.")
		print _("Use --help for instructions.")
		sys.exit(1)
	
	usage_string = _("Usage: %s <interface> <option> ...") % os.path.basename(sys.argv[0])
	parser = OptionParser(usage_string, add_help_option = False)
	parser.add_option('-h', '--help',
					action = "callback",
					callback = usage)
	parser.add_option('-b', '--backlight',
					dest = "backlight",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'status'])
	parser.add_option('-B', '--bluetooth',
					dest = "bluetooth",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'status'])
	parser.add_option('-c', '--cpu',
					dest = "cpu",
					type = "choice",
					choices = ['normal', 'silent', 'speed', 'cycle', 'hotkey', 'status'])
	parser.add_option('-w', '--webcam',
					dest = "webcam",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'status'])
	parser.add_option('-W', '--wireless',
					dest = "wireless",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'status'])
	parser.add_option('-n', '--show-notify',
					action = "store_true",
					dest = "show_notify",
					default = False)
	parser.add_option('-q', '--quiet',
					action = "store_true",
					dest = "quiet",
					default = False)
	parser.add_option('-s', '--stop-session',
					action = "store_true",
					dest = "stopsession",
					default = False)
	parser.add_option('-S', '--stop-system',
					action = "store_true",
					dest = "stopsystem",
					default = False)
	
	(options, args) = parser.parse_args()
	
	global quiet
	quiet = options.quiet
		
	if len(args) != 0:
		print _("Wrong argument(s).")
		print _("Use --help for instructions.")
		sys.exit(1)
	
	Backlight(options.backlight).apply()
	Bluetooth(options.bluetooth, options.show_notify).apply()
	Cpu(options.cpu, options.show_notify).apply()
	Webcam(options.webcam, options.show_notify).apply()
	Wireless(options.wireless, options.show_notify).apply()
	
	if options.stopsession == True:
		try:
			bus = dbus.SessionBus()
			proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_GENERAL)
			general = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
			general.Exit()
			if not quiet:
				print _("Session service stopped.")
		except:
			if not quiet:
				print _("Cannot stop session service.")
			pass
	
	if options.stopsystem == True:
		try:
			bus = dbus.SystemBus()
			proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_GENERAL)
			general = dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			general.Exit()
			if not quiet:
				print _("System service stopped.")
		except:
			if not quiet:
				print _("Cannot stop system service.")
			pass

if __name__ == "__main__":
	main()
