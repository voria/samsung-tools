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
sys.path.append('/usr/lib/samsung-tools')

from optparse import OptionParser

import dbus

from backends.globals import *

class Backlight():
	def __init__(self):
		bus = dbus.SessionBus()
		self.proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_BACKLIGHT)
		self.interface = dbus.Interface(self.proxy, SESSION_INTERFACE_NAME)
		
	def on(self):
		return self.interface.Enable()
	
	def off(self):
		return self.interface.Disable()
	
	def status(self):
		return self.interface.IsEnabled()
	
	def toggle(self):
		return self.interface.Toggle()	

class Bluetooth():
	def __init__(self):
		bus = dbus.SessionBus()
		self.proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_BLUETOOTH)
		self.interface = dbus.Interface(self.proxy, SESSION_INTERFACE_NAME)
	
	def is_available(self):
		return self.interface.IsAvailable()
	
	def on(self):
		return self.interface.Enable()
	
	def off(self):
		return self.interface.Disable()
	
	def toggle(self):
		return self.interface.Toggle()
		
	def status(self):
		return self.interface.IsEnabled()
		
class Fan():
	def __init__(self):
		bus = dbus.SessionBus()
		self.proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_FAN)
		self.interface = dbus.Interface(self.proxy, SESSION_INTERFACE_NAME)
	
	def is_available(self):
		return self.interface.IsAvailable()
	
	def normal(self):
		return self.interface.SetNormal()
	
	def silent(self):
		return self.interface.SetSilent()
	
	def speed(self):
		return self.interface.SetSpeed()
	
	def cycle(self):
		return self.interface.Cycle()
	
	def status(self):
		return self.interface.Status()
		
class Webcam():
	def __init__(self):
		bus = dbus.SessionBus()
		self.proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_WEBCAM)
		self.interface = dbus.Interface(self.proxy, SESSION_INTERFACE_NAME)
	
	def is_available(self):
		return self.interface.IsAvailable()
	
	def on(self):
		return self.interface.Enable()
	
	def off(self):
		return self.interface.Disable()
	
	def toggle(self):
		return self.interface.Toggle()
		
	def status(self):
		return self.interface.IsEnabled()

class Wireless():
	def __init__(self):
		# Connect to session bus
		bus = dbus.SessionBus()
		# Get proxy from samsung-tools' session service
		self.proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_WIRELESS)
		# Get interface from proxy
		self.interface = dbus.Interface(self.proxy, SESSION_INTERFACE_NAME)
	
	def is_available(self):
		return self.interface.IsAvailable()
	
	def on(self):
		return self.interface.Enable()
	
	def off(self):
		return self.interface.Disable()
	
	def toggle(self):
		return self.interface.Toggle()
		
	def status(self):
		return self.interface.IsEnabled()

def manage_backlight(option):
	if option == None:
		return	
	backlight = Backlight()
	if option == "on":
		result = backlight.on()
		if result == 1:
			print "Backlight enabled."
		else:
			print "ERROR: Backlight cannot be enabled."
	if option == "off":
		result = backlight.off()
		if result == 1:
			print "Backlight disabled."
		else:
			print "ERROR: Backlight cannot be disabled."
	if option == "toggle":
		result = backlight.toggle()
		if result == 1:
			print "Backlight toggled."
		else:
			print "ERROR: Backlight cannot be toggled."
	if option == "status":
		result = backlight.status()
		if result == 1:
			print "Backlight is currently enabled."
		else:
			print "Backlight is currently disabled."
	
def manage_bluetooth(option):
	if option == None:
		return
	bluetooth = Bluetooth()
	if not bluetooth.is_available():
		print "Bluetooth control is not available."
		return
	if option == "on":
		result = bluetooth.on()
		if result == 1:
			print "Bluetooth enabled."
		else:
			print "ERROR: Bluetooth cannot be enabled."
	if option == "off":
		result = bluetooth.off()
		if result == 1:
			print "Bluetooth disabled."
		else:
			print "ERROR: Bluetooth cannot be disabled."
	if option == "toggle":
		result = bluetooth.toggle()
		if result == 1:
			status = bluetooth.status()
			if status == 1:
				print "Bluetooth enabled."
			else:
				print "Bluetooth disabled."
		else:
			print "ERROR: Bluetooth cannot be toggled."
	if option == "status":
		result = bluetooth.status()
		if result == 1:
			print "Bluetooth is currently enabled."
		else:
			print "Bluetooth is currently disabled."
	
def manage_cpufan(option):
	if option == None:
		return
	fan = Fan()
	if not fan.is_available():
		print "CPU fan control is not available."
		return
	if option == "normal":
		result = fan.normal()
		if result == 1:
			print "CPU fan 'normal' mode enabled."
		else:
			print "ERROR: CPU fan 'normal' mode cannot be enabled."
	if option == "silent":
		result = fan.silent()
		if result == 1:
			print "CPU fan 'silent' mode enabled."
		else:
			print "ERROR: CPU fan 'silent' mode cannot be enabled."
	if option == "speed":
		result = fan.speed()
		if result == 1:
			print "CPU fan 'speed' mode enabled."
		else:
			print "ERROR: CPU fan 'speed' mode cannot be enabled."
	if option == "cycle":
		result = fan.cycle()
		if result == 1:
			mode = fan.status()
			if mode == 0:
				print "CPU fan mode switched to 'normal'."
			if mode == 1:
				print "CPU fan mode switched to 'silent'."
			if mode == 2:
				print "CPU fan mode switched to 'speed'."
			if mode == 3:
				print "ERROR: Cannot get new CPU fan status."
		else:
			print "ERROR: CPU fan mode cannot be switched." 
	if option == "status":
		result = fan.status()
		if result == 0:
			print "CPU fan current mode is 'normal'."
		if result == 1:
			print "CPU fan current mode is 'silent'."
		if result == 2:
			print "CPU fan current mode is 'speed'."
		if result == 3:
			print "ERROR: Cannot get current CPU fan status."  
	
def manage_webcam(option):
	if option == None:
		return
	webcam = Webcam()
	if not webcam.is_available():
		print "Webcam control is not available."
		return
	if option == "on":
		result = webcam.on()
		if result == 1:
			print "Webcam enabled."
		else:
			print "ERROR: Webcam cannot be enabled."
	if option == "off":
		result = webcam.off()
		if result == 1:
			print "Webcam disabled."
		else:
			print "ERROR: Webcam cannot be disabled."
	if option == "toggle":
		result = webcam.toggle()
		if result == 1:
			status = webcam.status()
			if status == 1:
				print "Webcam enabled."
			else:
				print "Webcam disabled."
		else:
			print "ERROR: Webcam cannot be toggled."
	if option == "status":
		result = webcam.status()
		if result == 1:
			print "Webcam is currently enabled."
		else:
			print "Webcam is currently disabled."
	
def manage_wireless(option):
	if option == None:
		return
	wireless = Wireless()
	if not wireless.is_available():
		print "Wireless control is not available."
		return
	if option == "on":
		result = wireless.on()
		if result == 1:
			print "Wireless enabled."
		else:
			print "ERROR: Wireless cannot be enabled."
	if option == "off":
		result = wireless.off()
		if result == 1:
			print "Wireless disabled."
		else:
			print "ERROR: Wireless cannot be disabled."
	if option == "toggle":
		result = wireless.toggle()
		if result == 1:
			status = wireless.status()
			if status == 1:
				print "Wireless enabled."
			else:
				print "Wireless disabled."
		else:
			print "ERROR: Wireless cannot be toggled."
	if option == "status":
		result = wireless.status()
		if result == 1:
			print "Wireless is currently enabled."
		else:
			print "Wireless is currently disabled."

def usage(option = None, opt = None, value = None, parser = None):
	print "Samsung-Tools - Command Line Utility"
	print
	print "Usage: %s <interface> <option> ..." % os.path.basename(sys.argv[0])
	print
	print "Backlight:"
	print "\tInterface:\t-b | --backlight"
	print "\tOptions:\ton | off | toggle | status"
	print "Bluetooth:"
	print "\tInterface:\t-B | --bluetooth"
	print "\tOptions:\ton | off | toggle | status"
	print "CPU Fan:"
	print "\tInterface:\t-f | --cpufan"
	print "\tOptions:\tnormal | silent | speed | cycle | status"
	print "Webcam:"
	print "\tInterface:\t-w | --webcam"
	print "\tOptions:\ton | off | toggle | status"
	print "Wireless:"
	print "\tInterface:\t-W | --wireless"
	print "\tOptions:\ton | off | toggle | status"
	print
	print "Examples of use:"
	print
	print " - Toggle backlight:"
	print "   %s --backlight toggle" % os.path.basename(sys.argv[0])
	print
	print " - Toggle wireless and set CPU fan to silent:"
	print "   %s --wireless toggle --cpufan silent" % os.path.basename(sys.argv[0])
	print
	print " - Disable bluetooth, webcam and wireless:"
	print "   %s -B off -w off -W off" % os.path.basename(sys.argv[0])	
	sys.exit()

def main():
	usage_string = "Usage: %s <interface> <option> ..." % os.path.basename(sys.argv[0])
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
	parser.add_option('-f', '--cpufan',
					dest = "cpufan",
					type = "choice",
					choices = ['normal', 'silent', 'speed', 'cycle', 'status'])
	parser.add_option('-w', '--webcam',
					dest = "webcam",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'status'])
	parser.add_option('-W', '--wireless',
					dest = "wireless",
					type = "choice",
					choices = ['on', 'off', 'toggle', 'status'])	
	
	(options, args) = parser.parse_args()
	
	if len(args) != 0:
		print "Wrong number of arguments."
		print "Use --help for instructions."
		sys.exit(1)
	
	if  len(sys.argv) == 1:
		print "No action(s) specified."
		print "Use --help for instructions."
		sys.exit(1)
	
	manage_backlight(options.backlight)
	manage_bluetooth(options.bluetooth)
	manage_cpufan(options.cpufan)
	manage_webcam(options.webcam)
	manage_wireless(options.wireless)

	## The following code kill session service, for developing purposes
	## TODO: Remember to remove it.
	#Connect to session bus
	bus = dbus.SessionBus()
	# Get proxy from session service
	general_proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_GENERAL)
	# Get interface from proxy
	general = dbus.Interface(general_proxy, SESSION_INTERFACE_NAME)
	# Quit the session service
	general.Exit()

if __name__ == "__main__":
	main()
