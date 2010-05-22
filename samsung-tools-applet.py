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
import dbus
import gtk
import gnomeapplet

import gettext
_ = gettext.gettext
gettext.bindtextdomain("samsung-tools")
gettext.textdomain("samsung-tools")

import sys
WORK_DIRECTORY = "/usr/lib/samsung-tools/"
sys.path.append(WORK_DIRECTORY)

from backends.globals import *
from backends.session.util.icons import *
from backends.session.util.locales import *

class Applet():
	def __init__(self, applet, iid):
		# Set panel icon
		pixbuf = gtk.gdk.pixbuf_new_from_file(SAMSUNG_TOOLS_ICON)
		pixbuf = pixbuf.scale_simple(22, 22, gtk.gdk.INTERP_BILINEAR)
		image = gtk.Image()
		image.set_from_pixbuf(pixbuf)
		eventbox = gtk.EventBox()
		eventbox.add(image)
		eventbox.set_has_tooltip(True)
		eventbox.set_tooltip_text("Samsung Tools")
		eventbox.set_visible_window(False)
		eventbox.connect("button-press-event", self.showMenu)
		applet.add(eventbox)
		
		builder = gtk.Builder()
		builder.set_translation_domain("samsung-tools")
		builder.add_from_file(os.path.join(WORK_DIRECTORY, "gui/glade/samsung-tools-applet.glade"))
				
		self.menu = builder.get_object("menu")
		self.bluetoothMenuitem = builder.get_object("bluetoothMenuitem")
		self.webcamMenuitem = builder.get_object("webcamMenuitem")
		self.wirelessMenuitem = builder.get_object("wirelessMenuitem")
		self.cpufanMenuitem = builder.get_object("cpufanMenuitem")
		self.preferencesMenuitem = builder.get_object("preferencesMenuitem")
	
		self.fanNormalRadiomenuitem = builder.get_object("fanNormalRadiomenuitem")
		self.fanSilentRadiomenuitem = builder.get_object("fanSilentRadiomenuitem")
		self.fanSpeedRadiomenuitem = builder.get_object("fanSpeedRadiomenuitem")
		
		self.bluetooth_sid = self.bluetoothMenuitem.connect("activate", self.on_bluetoothMenuitem_activate)
		self.webcam_sid = self.webcamMenuitem.connect("activate", self.on_webcamMenuitem_activate)
		self.wireless_sid = self.wirelessMenuitem.connect("activate", self.on_wirelessMenuitem_activate)
		self.fanNormal_sid = self.fanNormalRadiomenuitem.connect("toggled", self.on_fanRadiomenuitem_activate, "normal")
		self.fanSilent_sid = self.fanSilentRadiomenuitem.connect("toggled", self.on_fanRadiomenuitem_activate, "silent")
		self.fanSpeed_sid = self.fanSpeedRadiomenuitem.connect("toggled", self.on_fanRadiomenuitem_activate, "speed")
		self.preferencesMenuitem.connect("activate", self.on_preferencesMenuitem_activate)
		
		applet.set_background_widget(applet) # enable transparency hack

		
		applet.show_all()

	def __connect_bluetooth(self):
		""" Connect to session service for bluetooth control """
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_BLUETOOTH)
				return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
			except:
				retry = retry - 1
		sys.exit(1)
	
	def __connect_webcam(self):
		""" Connect to session service for webcam control """
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_WEBCAM)
				return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
			except:
				retry = retry - 1
		sys.exit(1)
	
	def __connect_wireless(self):
		""" Connect to session service for wireless control """
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_WIRELESS)
				return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
			except:
				retry = retry - 1
		sys.exit(1)
		
	def __connect_cpu(self):
		""" Connect to session service for cpu fan control """
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_CPU)
				return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
			except:
				retry = retry - 1
		sys.exit(1)

	def on_bluetoothMenuitem_activate(self, menuitem):
		conn = self.__connect_bluetooth()
		if menuitem.get_active() == True:
			conn.Enable(True)
		else:
			conn.Disable(True)
	
	def on_webcamMenuitem_activate(self, menuitem):
		conn = self.__connect_webcam()
		if menuitem.get_active() == True:
			conn.Enable(True)
		else:
			conn.Disable(True)
		
	def on_wirelessMenuitem_activate(self, menuitem):
		conn = self.__connect_wireless()
		if menuitem.get_active() == True:
			conn.Enable(True)
		else:
			conn.Disable(True)
		
	def on_preferencesMenuitem_activate(self, menuitem):
		import subprocess
		process = subprocess.Popen("samsung-tools-preferences", stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	
	def on_fanRadiomenuitem_activate(self, menuitem, data):
			conn = self.__connect_cpu()
			if data == "normal" and self.fanNormalRadiomenuitem.get_active() == True:
				conn.SetFanNormal(True)
			if data == "silent" and self.fanSilentRadiomenuitem.get_active() == True:
				conn.SetFanSilent(True)
			if data == "speed" and self.fanSpeedRadiomenuitem.get_active() == True:
				conn.SetFanSpeed(True)
	
	def showMenu(self, widget, event):
		if event.type == gtk.gdk.BUTTON_PRESS and event.button == 1:
			# Set bluetooth menuitem
			self.bluetoothMenuitem.handler_block(self.bluetooth_sid)
			conn = self.__connect_bluetooth()
			if not conn.IsAvailable():
				self.bluetoothMenuitem.set_sensitive(False)
			else:
				self.bluetoothMenuitem.set_sensitive(True)
				if conn.IsEnabled(False):
					self.bluetoothMenuitem.set_active(True)
				else:
					self.bluetoothMenuitem.set_active(False)
			self.bluetoothMenuitem.handler_unblock(self.bluetooth_sid)
			# Set webcam menuitem
			self.webcamMenuitem.handler_block(self.webcam_sid)
			conn = self.__connect_webcam()
			if not conn.IsAvailable():
				self.webcamMenuitem.set_sensitive(False)
			else:
				self.webcamMenuitem.set_sensitive(True)
				if conn.IsEnabled(False):
					self.webcamMenuitem.set_active(True)
				else:
					self.webcamMenuitem.set_active(False)
			self.webcamMenuitem.handler_unblock(self.webcam_sid)
			# Set wireless menuitem
			self.wirelessMenuitem.handler_block(self.wireless_sid)
			conn = self.__connect_wireless()
			if not conn.IsAvailable():
				self.wirelessMenuitem.set_sensitive(False)
			else:
				self.wirelessMenuitem.set_sensitive(True)
				if conn.IsEnabled(False):
					self.wirelessMenuitem.set_active(True)
				else:
					self.wirelessMenuitem.set_active(False)
			self.wirelessMenuitem.handler_unblock(self.wireless_sid)
			# Set CPU fan menuitem
			conn = self.__connect_cpu()
			if not conn.IsFanAvailable():
				self.cpufanMenuitem.set_sensitive(False)
			else:
				self.cpufanMenuitem.set_sensitive(True)
				# Set CPU fan radio buttons
				self.fanNormalRadiomenuitem.handler_block(self.fanNormal_sid)
				self.fanSilentRadiomenuitem.handler_block(self.fanSilent_sid)
				self.fanSpeedRadiomenuitem.handler_block(self.fanSpeed_sid)
				status = conn.Status(False)
				if status == 0:
					self.fanNormalRadiomenuitem.set_active(True)
				elif status == 1:
					self.fanSilentRadiomenuitem.set_active(True)
				elif status == 2:
					self.fanSpeedRadiomenuitem.set_active(True)
				self.fanNormalRadiomenuitem.handler_unblock(self.fanNormal_sid)
				self.fanSilentRadiomenuitem.handler_unblock(self.fanSilent_sid)
				self.fanSpeedRadiomenuitem.handler_unblock(self.fanSpeed_sid)
			if conn.IsTemperatureAvailable():
				temp = conn.GetTemperature()
				self.cpufanMenuitem.set_has_tooltip(True)
				self.cpufanMenuitem.set_tooltip_text(CPU_TEMPERATURE + " " + temp)
			# All ready, show menu	
			self.menu.popup(None, None, None, event.button, event.time)
		
if len(sys.argv) == 2:
	if sys.argv[1] == "--run-in-window":
		mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		mainWindow.set_title("Samsung Tools")
		mainWindow.connect("destroy", gtk.main_quit)
		applet = gnomeapplet.Applet()
		Applet(applet, None)
		applet.reparent(mainWindow)
		mainWindow.show_all()
		gtk.main()
		sys.exit()

if __name__ == '__main__':
	gnomeapplet.bonobo_factory("OAFIID:GNOME_SamsungTools_Applet", gnomeapplet.Applet.__gtype__, "Samsung Tools", "0", Applet)
