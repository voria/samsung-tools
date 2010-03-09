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
import time
import gtk
import gobject
import subprocess
import dbus

WORK_DIRECTORY = "/usr/lib/samsung-tools/"

import sys
sys.path.append(WORK_DIRECTORY)

import gettext
_ = gettext.gettext
gettext.bindtextdomain("samsung-tools")
gettext.textdomain("samsung-tools")

from backends.globals import *

# Popup (based on code from compizconfig-settings-manager)
class Popup (gtk.Window):
	def __init__ (self, text, title, parent = None):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
		self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
		self.set_title(title)
		if parent:
			self.set_transient_for(parent.get_toplevel())
		self.set_modal(True)
		self.set_decorated(True)
		self.set_property("skip-taskbar-hint", True)
		label = gtk.Label(text)
		align = gtk.Alignment()
		align.set_padding(20, 20, 20, 20)
		align.add(label)
		self.add(align)

# Key Grabber (based on code from compizconfig-settings-manager)
class KeyGrabber(gtk.Button):
	__gsignals__ = {"changed" : (gobject.SIGNAL_RUN_FIRST,
								gobject.TYPE_NONE,
								[gobject.TYPE_INT, gobject.TYPE_INT]),
					}
	def __init__ (self, label = None, popup_title = None):
		"""Prepare widget"""
		super(KeyGrabber, self).__init__()
		self.key = 0
		self.mods = 0
		self.handler = None
		self.label = label
		self.popup = None
		self.popup_title = popup_title
		self.connect("clicked", self.begin_key_grab)
		self.set_label()

	def begin_key_grab(self, widget):
		self.add_events(gtk.gdk.KEY_PRESS_MASK)
		self.popup = Popup(_("Please press the new key combination"), self.popup_title, self)
		self.popup.show_all()
		self.handler = self.popup.connect("key-press-event", self.on_key_press_event)
		while gtk.gdk.keyboard_grab(self.popup.window) != gtk.gdk.GRAB_SUCCESS:
			time.sleep(0.1)

	def end_key_grab(self):
		gtk.gdk.keyboard_ungrab(gtk.get_current_event_time())
		self.popup.disconnect(self.handler)
		self.popup.destroy()

	def on_key_press_event(self, widget, event):
		mods = event.state & gtk.accelerator_get_default_mod_mask()

		if event.keyval in (gtk.keysyms.Escape, gtk.keysyms.Return) and not mods:
			self.end_key_grab()
			self.set_label(self.key, self.mods)
			return

		key = gtk.gdk.keyval_to_lower(event.keyval)
		if (key == gtk.keysyms.ISO_Left_Tab):
			key = gtk.keysyms.Tab

		if gtk.accelerator_valid(key, mods) or (key == gtk.keysyms.Tab and mods):
			self.set_label(key, mods, True)
			self.end_key_grab()
			return

		self.set_label(key, mods)

	def set_label(self, key = None, mods = None, valid = False):
		if key != None and mods != None:
			# emit 'changed' signal only when key is validated (valud = True)
			if valid:
				self.key = key
				self.mods = mods
				self.emit("changed", self.key, self.mods)
		if key == None and mods == None:
			key = self.key
			mods = self.mods
		label = gtk.accelerator_name(key, mods)
		if not len(label):
			label = _("None")
		else:
			if label == "XF86Sleep":
				label = "Fn-Esc"
			if label == "XF86Battery":
				label = "Fn-F2"
			if label == "<Alt>KP_Insert":
				label = "Fn-F3"
			if label == "XF86Launch4":
				label = "Fn-F4"
			if label == "XF86Launch1":
				label = "Fn-F5"
			if label == "XF86AudioMute":
				label = "Fn-F6"
			if label == "XF86Launch2":
				label = "Fn-F7"
			if label == "XF86Launch3":
				label = "Fn-F8"
			if label == "XF86WLAN":
				label = "Fn-F9"
		gtk.Button.set_label(self, label)
	
class Main():
	def __init__(self):
		# Get interfaces for D-Bus services
		session = self.__connect_session()
		system = self.__connect_system()

		# Setup GUI
		self.builder = gtk.Builder()
		self.builder.set_translation_domain("samsung-tools")
		self.builder.add_from_file(os.path.join(WORK_DIRECTORY, "gui/glade/samsung-tools-preferences.glade"))
		
		###
		### Main widgets
		###
		self.mainWindow = self.builder.get_object("mainWindow")
		self.mainWindow.connect("delete-event", self.quit)
		self.closeButton = self.builder.get_object("closeButton")
		self.closeButton.connect("clicked", self.quit)
		self.aboutButton = self.builder.get_object("aboutButton")
		self.aboutButton.connect("clicked", self.about)
	
		###
		### Session configuration
		###
		self.sessionTable = self.builder.get_object("sessionTable")
		# Set backlight hotkey grabber
		self.backlightHotkeyButton = KeyGrabber(popup_title = "Backlight control")
		hotkey = session.GetBacklightHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.backlightHotkeyButton.set_label(key, mods, True)
		self.backlightHotkeyButton.set_tooltip_text(self.builder.get_object("backlightHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.backlightHotkeyButton, 1, 2, 2, 3, yoptions = 0)
		self.backlightHotkeyButton.connect("changed", self.on_backlightHotkeyButton_changed)
		self.backlightHotkeyButton.show()
		# Set bluetooth hotkey grabber
		self.bluetoothHotkeyButton = KeyGrabber(popup_title = "Bluetooth control")
		hotkey = session.GetBluetoothHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.bluetoothHotkeyButton.set_label(key, mods, True)
		self.bluetoothHotkeyButton.set_tooltip_text(self.builder.get_object("bluetoothHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.bluetoothHotkeyButton, 1, 2, 3, 4, yoptions = 0)
		self.bluetoothHotkeyButton.connect("changed", self.on_bluetoothHotkeyButton_changed)
		self.bluetoothHotkeyButton.show()
		# Set cpu hotkey grabber
		self.cpuHotkeyButton = KeyGrabber(popup_title = _("CPU/Fan"))
		hotkey = session.GetCpuHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.cpuHotkeyButton.set_label(key, mods, True)
		self.cpuHotkeyButton.set_tooltip_text(self.builder.get_object("cpuHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.cpuHotkeyButton, 1, 2, 4, 5, yoptions = 0)
		self.cpuHotkeyButton.connect("changed", self.on_cpuHotkeyButton_changed)
		self.cpuHotkeyButton.show()
		# Set webcam hotkey grabber
		self.webcamHotkeyButton = KeyGrabber(popup_title = _("Webcam"))
		hotkey = session.GetWebcamHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.webcamHotkeyButton.set_label(key, mods, True)
		self.webcamHotkeyButton.set_tooltip_text(self.builder.get_object("webcamHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.webcamHotkeyButton, 1, 2, 5, 6, yoptions = 0)
		self.webcamHotkeyButton.connect("changed", self.on_webcamHotkeyButton_changed)
		self.webcamHotkeyButton.show()
		# Set wireless hotkey grabber
		self.wirelessHotkeyButton = KeyGrabber(popup_title = _("Wireless"))
		hotkey = session.GetWirelessHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.wirelessHotkeyButton.set_label(key, mods, True)
		self.wirelessHotkeyButton.set_tooltip_text(self.builder.get_object("wirelessHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.wirelessHotkeyButton, 1, 2, 6, 7, yoptions = 0)
		self.wirelessHotkeyButton.connect("changed", self.on_wirelessHotkeyButton_changed)
		self.wirelessHotkeyButton.show()
		# Set clean buttons for keygrabbers
		self.backlightHotkeyCleanButton = self.builder.get_object("backlightHotkeyCleanButton")
		self.backlightHotkeyCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
		self.backlightHotkeyCleanButton.connect("clicked", self.on_backlightHotkeyCleanButton_clicked)
		self.bluetoothHotkeyCleanButton = self.builder.get_object("bluetoothHotkeyCleanButton")
		self.bluetoothHotkeyCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
		self.bluetoothHotkeyCleanButton.connect("clicked", self.on_bluetoothHotkeyCleanButton_clicked)
		self.cpuHotkeyCleanButton = self.builder.get_object("cpuHotkeyCleanButton")
		self.cpuHotkeyCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
		self.cpuHotkeyCleanButton.connect("clicked", self.on_cpuHotkeyCleanButton_clicked)
		self.webcamHotkeyCleanButton = self.builder.get_object("webcamHotkeyCleanButton")
		self.webcamHotkeyCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
		self.webcamHotkeyCleanButton.connect("clicked", self.on_webcamHotkeyCleanButton_clicked)
		self.wirelessHotkeyCleanButton = self.builder.get_object("wirelessHotkeyCleanButton")
		self.wirelessHotkeyCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
		self.wirelessHotkeyCleanButton.connect("clicked", self.on_wirelessHotkeyCleanButton_clicked)
		# Set default buttons for keygrabbers
		self.backlightHotkeyDefaultButton = self.builder.get_object("backlightHotkeyDefaultButton")
		self.backlightHotkeyDefaultButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.backlightHotkeyDefaultButton.connect("clicked", self.on_backlightHotkeyDefaultButton_clicked)
		self.bluetoothHotkeyDefaultButton = self.builder.get_object("bluetoothHotkeyDefaultButton")
		self.bluetoothHotkeyDefaultButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.bluetoothHotkeyDefaultButton.connect("clicked", self.on_bluetoothHotkeyDefaultButton_clicked)
		self.cpuHotkeyDefaultButton = self.builder.get_object("cpuHotkeyDefaultButton")
		self.cpuHotkeyDefaultButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.cpuHotkeyDefaultButton.connect("clicked", self.on_cpuHotkeyDefaultButton_clicked)
		self.webcamHotkeyDefaultButton = self.builder.get_object("webcamHotkeyDefaultButton")
		self.webcamHotkeyDefaultButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.webcamHotkeyDefaultButton.connect("clicked", self.on_webcamHotkeyDefaultButton_clicked)
		self.wirelessHotkeyDefaultButton = self.builder.get_object("wirelessHotkeyDefaultButton")
		self.wirelessHotkeyDefaultButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.wirelessHotkeyDefaultButton.connect("clicked", self.on_wirelessHotkeyDefaultButton_clicked)
		# Set enable hotkeys checkbutton
		self.backlightHotkeyLabel = self.builder.get_object("backlightHotkeyLabel")
		self.bluetoothHotkeyLabel = self.builder.get_object("bluetoothHotkeyLabel")
		self.cpuHotkeyLabel = self.builder.get_object("cpuHotkeyLabel")
		self.webcamHotkeyLabel = self.builder.get_object("webcamHotkeyLabel")
		self.wirelessHotkeyLabel = self.builder.get_object("wirelessHotkeyLabel")
		self.useHotkeysCheckbutton = self.builder.get_object("useHotkeysCheckbutton")
		if session.GetUseHotkeys() == "true":
			self.useHotkeysCheckbutton.set_active(True)
		else:
			self.useHotkeysCheckbutton.set_active(False)
		self.useHotkeysCheckbutton.connect("toggled", self.on_useHotkeysCheckbutton_toggled)
		self.on_useHotkeysCheckbutton_toggled(self.useHotkeysCheckbutton, True)
		
		###
		### System configuration
		###
		# Last status restore
		self.lastStatusRestoreCombobox = self.builder.get_object("lastStatusRestoreCombobox")
		# Set cell renderer for 'last status restore' combobox
		self.lastStatusRestoreComboboxCR = gtk.CellRendererText()
		self.lastStatusRestoreCombobox.pack_start(self.lastStatusRestoreComboboxCR)
		self.lastStatusRestoreCombobox.add_attribute(self.lastStatusRestoreComboboxCR, 'text', 0)
		if system.GetLastStatusRestore() == "true":
			self.lastStatusRestoreCombobox.set_active(0)
		else: # laststatusrestore == "false"
			self.lastStatusRestoreCombobox.set_active(1)
		self.lastStatusRestoreCombobox.connect("changed", self.on_lastStatusRestoreCombobox_changed)
		# Wireless toggle method
		self.wirelessToggleMethodCombobox = self.builder.get_object("wirelessToggleMethodCombobox")
		# Set cell renderer for 'wireless toggle method' combobox
		self.wirelessToggleMethodComboboxCR = gtk.CellRendererText()
		self.wirelessToggleMethodCombobox.pack_start(self.wirelessToggleMethodComboboxCR)
		self.wirelessToggleMethodCombobox.add_attribute(self.wirelessToggleMethodComboboxCR, 'text', 0)
		wirelesstogglemethod = system.GetWirelessToggleMethod()
		if wirelesstogglemethod == "iwconfig":
			self.wirelessToggleMethodCombobox.set_active(0)
		elif wirelesstogglemethod == "module":
			self.wirelessToggleMethodCombobox.set_active(1)
		else: # wirelesstogglemethod == "esdm"
			self.wirelessToggleMethodCombobox.set_active(2)
		self.wirelessToggleMethodCombobox.connect("changed", self.on_wirelessToggleMethodCombobox_changed)
		# Wireless device
		self.wirelessDeviceEntry = self.builder.get_object("wirelessDeviceEntry")
		self.wirelessDeviceEntry.set_text(system.GetWirelessDevice())
		self.wirelessDeviceEntry.connect("focus-out-event", self.on_wirelessDeviceEntry_focus_out_event)
		# Wireless module
		self.wirelessModuleEntry = self.builder.get_object("wirelessModuleEntry")
		self.wirelessModuleEntry.set_text(system.GetWirelessModule())
		self.wirelessModuleEntry.connect("focus-out-event", self.on_wirelessModuleEntry_focus_out_event)
		# Set clean buttons
		self.lastStatusRestoreCleanButton = self.builder.get_object("lastStatusRestoreCleanButton")
		self.lastStatusRestoreCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.lastStatusRestoreCleanButton.connect("clicked", self.on_lastStatusRestoreCleanButton_clicked)
		self.wirelessToggleMethodCleanButton = self.builder.get_object("wirelessToggleMethodCleanButton")
		self.wirelessToggleMethodCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.wirelessToggleMethodCleanButton.connect("clicked", self.on_wirelessToggleMethodCleanButton_clicked)
		self.wirelessDeviceCleanButton = self.builder.get_object("wirelessDeviceCleanButton")
		self.wirelessDeviceCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.wirelessDeviceCleanButton.connect("clicked", self.on_wirelessDeviceCleanButton_clicked)
		self.wirelessModuleCleanButton = self.builder.get_object("wirelessModuleCleanButton")
		self.wirelessModuleCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.wirelessModuleCleanButton.connect("clicked", self.on_wirelessModuleCleanButton_clicked)
		# Disable 'wireless device' and 'wireless module' options according to 'wireless toggle method' status
		active_method = self.wirelessToggleMethodCombobox.get_active()
		if active_method == 0:
			self.wirelessDeviceEntry.set_sensitive(True)
			self.wirelessDeviceCleanButton.set_sensitive(True)
			self.wirelessModuleEntry.set_sensitive(False)
			self.wirelessModuleCleanButton.set_sensitive(False)
		elif active_method == 1:
			self.wirelessDeviceEntry.set_sensitive(False)
			self.wirelessDeviceCleanButton.set_sensitive(False)
			self.wirelessModuleEntry.set_sensitive(True)
			self.wirelessModuleCleanButton.set_sensitive(True)
		else:
			self.wirelessDeviceEntry.set_sensitive(False)
			self.wirelessDeviceCleanButton.set_sensitive(False)
			self.wirelessModuleEntry.set_sensitive(False)
			self.wirelessModuleCleanButton.set_sensitive(False)
		
		# All ready
		self.mainWindow.show()
	
	def __connect_session(self):
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SessionBus()
				proxy = bus.get_object(SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_OPTIONS)
				return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
			except:
				retry = retry - 1
		print _("Unable to connect to session service!")
		sys.exit(1)
		
	def __connect_system(self):
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_OPTIONS)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		print _("Unable to connect to system service!")
		sys.exit(1)
	
	def __convert_gtk_to_xbindkeys(self, hotkey):
		keys = hotkey.replace('<', "").split('>')
		result = ""
		for key in keys:
			if key == "Super":
				key = "Mod4"
			result += key + "+"
		result = result[0:len(result) - 1] # Remove the '+' at the end
		return result
	
	def __convert_xbindkeys_to_gtk(self, hotkey):
		keys = hotkey.split('+')
		result = ""
		for key in keys:
			key = key.strip()
			if key == "Mod4":
				key = "Super"
			if key == "Control" or key == "Shift" or key == "Alt" or key == "Super":
				result += "<"
			result += key
			if key == "Control" or key == "Shift" or key == "Alt" or key == "Super":
				result += ">"
		return result
	
	def on_useHotkeysCheckbutton_toggled(self, checkbutton = None, toggle_widgets_only = False):
		self.backlightHotkeyLabel.set_sensitive(checkbutton.get_active())
		self.bluetoothHotkeyLabel.set_sensitive(checkbutton.get_active())
		self.cpuHotkeyLabel.set_sensitive(checkbutton.get_active())
		self.webcamHotkeyLabel.set_sensitive(checkbutton.get_active())
		self.wirelessHotkeyLabel.set_sensitive(checkbutton.get_active())
		
		self.backlightHotkeyButton.set_sensitive(checkbutton.get_active())
		self.bluetoothHotkeyButton.set_sensitive(checkbutton.get_active())
		self.cpuHotkeyButton.set_sensitive(checkbutton.get_active())
		self.webcamHotkeyButton.set_sensitive(checkbutton.get_active())
		self.wirelessHotkeyButton.set_sensitive(checkbutton.get_active())
		
		self.backlightHotkeyCleanButton.set_sensitive(checkbutton.get_active())
		self.bluetoothHotkeyCleanButton.set_sensitive(checkbutton.get_active())
		self.cpuHotkeyCleanButton.set_sensitive(checkbutton.get_active())
		self.webcamHotkeyCleanButton.set_sensitive(checkbutton.get_active())
		self.wirelessHotkeyCleanButton.set_sensitive(checkbutton.get_active())
		
		self.backlightHotkeyDefaultButton.set_sensitive(checkbutton.get_active())
		self.bluetoothHotkeyDefaultButton.set_sensitive(checkbutton.get_active())
		self.cpuHotkeyDefaultButton.set_sensitive(checkbutton.get_active())
		self.webcamHotkeyDefaultButton.set_sensitive(checkbutton.get_active())
		self.wirelessHotkeyDefaultButton.set_sensitive(checkbutton.get_active())
		
		if toggle_widgets_only == False:
			session = self.__connect_session()
			if checkbutton.get_active() == True:
				session.SetUseHotkeys("true")
			else:
				session.SetUseHotkeys("false")
	
	def on_backlightHotkeyButton_changed(self, button = None, key = None, mods = None):
		if key == 0 and mods == 0:
			new = "disable"
		else:
			new = gtk.accelerator_name(key, mods)
		session = self.__connect_session()
		session.SetBacklightHotkey(self.__convert_gtk_to_xbindkeys(new))
		
	
	def on_bluetoothHotkeyButton_changed(self, button = None, key = None, mods = None):
		if key == 0 and mods == 0:
			new = "disable"
		else:
			new = gtk.accelerator_name(key, mods) 
		session = self.__connect_session()
		session.SetBluetoothHotkey(self.__convert_gtk_to_xbindkeys(new))
		
	def on_cpuHotkeyButton_changed(self, button = None, key = None, mods = None):
		if key == 0 and mods == 0:
			new = "disable"
		else:
			new = gtk.accelerator_name(key, mods) 
		session = self.__connect_session()
		session.SetCpuHotkey(self.__convert_gtk_to_xbindkeys(new))
		
	def on_webcamHotkeyButton_changed(self, button = None, key = None, mods = None):
		if key == 0 and mods == 0:
			new = "disable"
		else:
			new = gtk.accelerator_name(key, mods) 
		session = self.__connect_session()
		session.SetWebcamHotkey(self.__convert_gtk_to_xbindkeys(new))
		
	def on_wirelessHotkeyButton_changed(self, button = None, key = None, mods = None):
		if key == 0 and mods == 0:
			new = "disable"
		else:
			new = gtk.accelerator_name(key, mods) 
		session = self.__connect_session()
		session.SetWirelessHotkey(self.__convert_gtk_to_xbindkeys(new))
	
	def on_backlightHotkeyCleanButton_clicked(self, button = None):
		self.backlightHotkeyButton.set_label(0, 0, True)
	
	def on_bluetoothHotkeyCleanButton_clicked(self, button = None):
		self.bluetoothHotkeyButton.set_label(0, 0, True)
	
	def on_cpuHotkeyCleanButton_clicked(self, button = None):
		self.cpuHotkeyButton.set_label(0, 0, True)
	
	def on_webcamHotkeyCleanButton_clicked(self, button = None):
		self.webcamHotkeyButton.set_label(0, 0, True)
	
	def on_wirelessHotkeyCleanButton_clicked(self, button = None):
		self.wirelessHotkeyButton.set_label(0, 0, True)
	
	def on_backlightHotkeyDefaultButton_clicked(self, button = None):
		session = self.__connect_session()
		session.SetBacklightHotkey("default")
		hotkey = session.GetBacklightHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.backlightHotkeyButton.set_label(key, mods, True)
	
	def on_bluetoothHotkeyDefaultButton_clicked(self, button = None):
		session = self.__connect_session()
		session.SetBluetoothHotkey("default")
		hotkey = session.GetBluetoothHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.bluetoothHotkeyButton.set_label(key, mods, True)
	
	def on_cpuHotkeyDefaultButton_clicked(self, button = None):
		session = self.__connect_session()
		session.SetCpuHotkey("default")
		hotkey = session.GetCpuHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.cpuHotkeyButton.set_label(key, mods, True)
	
	def on_webcamHotkeyDefaultButton_clicked(self, button = None):
		session = self.__connect_session()
		session.SetWebcamHotkey("default")
		hotkey = session.GetWebcamHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.webcamHotkeyButton.set_label(key, mods, True)
	
	def on_wirelessHotkeyDefaultButton_clicked(self, button = None):
		session = self.__connect_session()
		session.SetWirelessHotkey("default")
		hotkey = session.GetWirelessHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.wirelessHotkeyButton.set_label(key, mods, True)
	
	def on_lastStatusRestoreCombobox_changed(self, combobox = None):
		system = self.__connect_system()
		if combobox.get_active() == 0:
			system.SetLastStatusRestore("true")
		else:
			system.SetLastStatusRestore("false")
	
	def on_wirelessToggleMethodCombobox_changed(self, combobox = None):
		system = self.__connect_system()
		active = combobox.get_active()
		if active == 0:
			system.SetWirelessToggleMethod("iwconfig")
			self.wirelessDeviceEntry.set_sensitive(True)
			self.wirelessDeviceCleanButton.set_sensitive(True)
			self.wirelessModuleEntry.set_sensitive(False)
			self.wirelessModuleCleanButton.set_sensitive(False)
		elif active == 1:
			system.SetWirelessToggleMethod("module")
			self.wirelessDeviceEntry.set_sensitive(False)
			self.wirelessDeviceCleanButton.set_sensitive(False)
			self.wirelessModuleEntry.set_sensitive(True)
			self.wirelessModuleCleanButton.set_sensitive(True)
		else:
			system.SetWirelessToggleMethod("esdm")
			self.wirelessDeviceEntry.set_sensitive(False)
			self.wirelessDeviceCleanButton.set_sensitive(False)
			self.wirelessModuleEntry.set_sensitive(False)
			self.wirelessModuleCleanButton.set_sensitive(False)
		
	def on_wirelessDeviceEntry_focus_out_event(self, widget = None, event = None):
		new = widget.get_text()
		system = self.__connect_system()
		if new == "":
			widget.set_text(system.GetWirelessDevice())
			return
		old = system.GetWirelessDevice()
		if new != old:
			system.SetWirelessDevice(new)
	
	def on_wirelessModuleEntry_focus_out_event(self, widget = None, event = None):
		new = widget.get_text()
		system = self.__connect_system()
		if new == "":
			widget.set_text(system.GetWirelessModule())
			return
		old = system.GetWirelessModule()
		if new != old:
			system.SetWirelessModule(new)
	
	def on_lastStatusRestoreCleanButton_clicked(self, button = None):
		if self.lastStatusRestoreCombobox.get_active() != 0:
			self.lastStatusRestoreCombobox.set_active(0)
	
	def on_wirelessToggleMethodCleanButton_clicked(self, button = None):
		if self.wirelessToggleMethodCombobox.get_active() != 0:
			self.wirelessToggleMethodCombobox.set_active(0)
	
	def on_wirelessDeviceCleanButton_clicked(self, button = None):
		system = self.__connect_system()
		system.SetWirelessDevice("default")
		self.wirelessDeviceEntry.set_text(system.GetWirelessDevice())
	
	def on_wirelessModuleCleanButton_clicked(self, button = None):
		system = self.__connect_system()
		system.SetWirelessModule("default")
		self.wirelessModuleEntry.set_text(system.GetWirelessModule())
	
	def about(self, button = None):
		dialog = gtk.AboutDialog()
		dialog.set_name(APP_NAME)
		dialog.set_version(APP_VERSION)
		copyright = _("Released under GPLv3 license") + "\n\nCopyleft by\nFortunato Ventre (voRia)\nvorione@gmail.com"
		dialog.set_copyright(copyright)
		dialog.set_website("http://www.voria.org/forum")
		dialog.set_website_label("Linux On My Samsung")
		dialog.run()
		dialog.destroy()
	
	def quit(self, widget = None, event = None):
		gtk.main_quit()
	
if __name__ == "__main__":
	Main()
	gtk.main()
