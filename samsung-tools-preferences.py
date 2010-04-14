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
from backends.session.util.icons import * 

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
		self.popup = Popup(_("Please press the new hotkey"), self.popup_title, self)
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
			if label == "XF86Launch4" or label == "XF86Display":
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

class LaptopModeDialog():
	def __init__(self, parent):
		# Setup GUI
		self.builder = gtk.Builder()
		self.builder.set_translation_domain("samsung-tools")
		self.builder.add_from_file(os.path.join(WORK_DIRECTORY, "gui/glade/samsung-tools-preferences-laptop-mode.glade"))
		
		self.mainDialog = self.builder.get_object("mainDialog")
		self.mainDialog.set_icon_from_file(SAMSUNG_TOOLS_ICON)
		self.mainDialog.set_transient_for(parent)
		self.mainDialog.connect("delete-event", self.quit)
		
		self.closeButton = self.builder.get_object("closeButton")
		self.closeButton.connect("clicked", self.quit)
		
		laptopModeTable = self.builder.get_object("laptopModeTable")
		laptopmode = self.__connect()
		# USB autosuspend
		self.usbAutosuspendCheckbutton = self.builder.get_object("usbAutosuspendCheckbutton")
		option = laptopmode.GetUSBAutosuspend()
		if option == 1:
			self.usbAutosuspendCheckbutton.set_active(True)
		self.usbAutosuspendCheckbutton.connect("toggled", self.on_usbAutosuspendCheckbutton_toggled)
		# HAL polling
		self.halPollingCheckbutton = self.builder.get_object("halPollingCheckbutton")
		option = laptopmode.GetHalPolling()
		if option == 1:
			self.halPollingCheckbutton.set_active(True)
		self.halPollingCheckbutton.connect("toggled", self.on_halPollingCheckbutton_toggled)
		# Ethernet
		self.ethernetCheckbutton = self.builder.get_object("ethernetCheckbutton")
		option = laptopmode.GetEthernet()
		if option == 1:
			self.ethernetCheckbutton.set_active(True)
		self.ethernetCheckbutton.connect("toggled", self.on_ethernetCheckbutton_toggled)
		# Sound
		self.intelHDAPowerCheckbutton = self.builder.get_object("intelHDAPowerCheckbutton")
		option = laptopmode.GetIntelHDAPower()
		if option == 1:
			self.intelHDAPowerCheckbutton.set_active(True)
		self.intelHDAPowerCheckbutton.connect("toggled", self.on_intelHDAPowerCheckbutton_toggled)
		# SATA
		self.intelSATAPowerCheckbutton = self.builder.get_object("intelSATAPowerCheckbutton")
		option = laptopmode.GetIntelSATAPower()
		if option == 1:
			self.intelSATAPowerCheckbutton.set_active(True)
		self.intelSATAPowerCheckbutton.connect("toggled", self.on_intelSATAPowerCheckbutton_toggled)
		# Configuration files
		self.configFilesCheckbutton = self.builder.get_object("configFilesCheckbutton")
		option = laptopmode.GetConfigFilesControl()
		if option == 1:
			self.configFilesCheckbutton.set_active(True)
		self.configFilesCheckbutton.connect("toggled", self.on_configFilesCheckbutton_toggled)
		# Video output
		self.videoOutputCheckbutton = self.builder.get_object("videoOutputCheckbutton")
		option = laptopmode.GetVideoOutput()
		if option == 1:
			self.videoOutputCheckbutton.set_active(True)
		self.videoOutputCheckbutton.connect("toggled", self.on_videoOutputCheckbutton_toggled)
		# Linux scheduler
		self.schedMcPowerCheckbutton = self.builder.get_object("schedMcPowerCheckbutton")
		option = laptopmode.GetSchedMcPower()
		if option == 1:
			self.schedMcPowerCheckbutton.set_active(True)
		self.schedMcPowerCheckbutton.connect("toggled", self.on_schedMcPowerCheckbutton_toggled)
		# HD power management
		self.hdPowerMgmtSpinbutton = self.builder.get_object("hdPowerMgmtSpinbutton")
		self.hdPowerMgmtSpinbuttonValue = laptopmode.GetHDPowerMgmt()
		self.hdPowerMgmtSpinbutton.set_value(self.hdPowerMgmtSpinbuttonValue)
		self.hdPowerMgmtSpinbutton.connect("value-changed", self.on_hdPowerMgmtSpinbutton_valuechanged)

		self.mainDialog.run()
	
	def __connect(self):
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_LAPTOPMODE)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		print unicode(_("Unable to connect to system service!"), "utf-8")
		sys.exit(1)
	
	def on_usbAutosuspendCheckbutton_toggled(self, checkbutton):
		conn = self.__connect()
		if checkbutton.get_active() == True:
			conn.SetUSBAutosuspend(1)
		else:
			conn.SetUSBAutosuspend(0)
	
	def on_halPollingCheckbutton_toggled(self, checkbutton):
		conn = self.__connect()
		if checkbutton.get_active() == True:
			conn.SetHalPolling(1)
		else:
			conn.SetHalPolling(0)
	
	def on_ethernetCheckbutton_toggled(self, checkbutton):
		conn = self.__connect()
		if checkbutton.get_active() == True:
			conn.SetEthernet(1)
		else:
			conn.SetEthernet(0)
	
	def on_intelHDAPowerCheckbutton_toggled(self, checkbutton):
		conn = self.__connect()
		if checkbutton.get_active() == True:
			conn.SetIntelHDAPower(1)
		else:
			conn.SetIntelHDAPower(0)
	
	def on_intelSATAPowerCheckbutton_toggled(self, checkbutton):
		conn = self.__connect()
		if checkbutton.get_active() == True:
			conn.SetIntelSATAPower(1)
		else:
			conn.SetIntelSATAPower(0)
	
	def on_configFilesCheckbutton_toggled(self, checkbutton):
		conn = self.__connect()
		if checkbutton.get_active() == True:
			conn.SetConfigFilesControl(1)
		else:
			conn.SetConfigFilesControl(0)
	
	def on_videoOutputCheckbutton_toggled(self, checkbutton):
		conn = self.__connect()
		if checkbutton.get_active() == True:
			conn.SetVideoOutput(1)
		else:
			conn.SetVideoOutput(0)

	def on_schedMcPowerCheckbutton_toggled(self, checkbutton):
		conn = self.__connect()
		if checkbutton.get_active() == True:
			conn.SetSchedMcPower(1)
		else:
			conn.SetSchedMcPower(0)
	
	def on_hdPowerMgmtSpinbutton_valuechanged(self, button, event = None):
		self.hdPowerMgmtSpinbuttonValue = button.get_value_as_int()
		# Value will be actually saved at the time the dialog is quitted
	
	def quit(self, widget = None, event = None):
		conn = self.__connect()
		conn.SetHDPowerMgmt(self.hdPowerMgmtSpinbuttonValue)
		conn.RestartDaemon()
		self.mainDialog.destroy()

class KernelParametersDialog():
	def __init__(self, parent):
		# Setup GUI
		self.builder = gtk.Builder()
		self.builder.set_translation_domain("samsung-tools")
		self.builder.add_from_file(os.path.join(WORK_DIRECTORY, "gui/glade/samsung-tools-preferences-kernel-parameters.glade"))
		
		self.mainDialog = self.builder.get_object("mainDialog")
		self.mainDialog.set_icon_from_file(SAMSUNG_TOOLS_ICON)
		self.mainDialog.set_transient_for(parent)
		self.mainDialog.connect("delete-event", self.quit)
		
		self.closeButton = self.builder.get_object("closeButton")
		self.closeButton.connect("clicked", self.quit)
		
		# Swappiness
		conn = self.__connect()
		self.swappinessSpinbutton = self.builder.get_object("swappinessSpinbutton")
		self.swappinessSpinbuttonValue = conn.GetSwappiness()
		self.swappinessSpinbutton.set_value(self.swappinessSpinbuttonValue)
		self.swappinessSpinbutton.connect("value-changed", self.on_swappinessSpinbutton_valuechanged)
		
		self.mainDialog.run()
	
	def __connect(self):
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_SYSCTL)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		print unicode(_("Unable to connect to system service!"), "utf-8")
		sys.exit(1)

	def on_swappinessSpinbutton_valuechanged(self, button, event = None):
		self.swappinessSpinbuttonValue = button.get_value_as_int()
		# Value will be actually saved at the time the dialog is quitted
	
	def quit(self, widget = None, event = None):
		conn = self.__connect()
		conn.SetSwappiness(self.swappinessSpinbuttonValue)
		conn.ApplySettings()
		self.mainDialog.destroy()

class PhcDialog():
	def __init__(self, parent):
		# Setup GUI
		self.builder = gtk.Builder()
		self.builder.set_translation_domain("samsung-tools")
		self.builder.add_from_file(os.path.join(WORK_DIRECTORY, "gui/glade/samsung-tools-preferences-phc.glade"))
		
		self.mainDialog = self.builder.get_object("mainDialog")
		self.mainDialog.set_icon_from_file(SAMSUNG_TOOLS_ICON)
		self.mainDialog.set_transient_for(parent)
		self.mainDialog.connect("delete-event", self.quit)
		
		self.closeButton = self.builder.get_object("closeButton")
		self.closeButton.connect("clicked", self.quit)
		
		self.applyAtBootCheckbutton = self.builder.get_object("applyAtBootCheckbutton")
		conn = self.__connect_options()
		if conn.GetPHCVids() != "":
			self.applyAtBootCheckbutton.set_active(True)
		
		# Get all remaining widgets
		self.freqLabels = [
						self.builder.get_object("freq1Label"),
						self.builder.get_object("freq2Label"),
						self.builder.get_object("freq3Label"),
						self.builder.get_object("freq4Label"),
						self.builder.get_object("freq5Label")
						]
		self.defaultVidLabels = [
								self.builder.get_object("defaultVid1Label"),
								self.builder.get_object("defaultVid2Label"),
								self.builder.get_object("defaultVid3Label"),
								self.builder.get_object("defaultVid4Label"),
								self.builder.get_object("defaultVid5Label")
								]
		self.vidSpinbuttons = [
							self.builder.get_object("vid1Spinbutton"),
							self.builder.get_object("vid2Spinbutton"),
							self.builder.get_object("vid3Spinbutton"),
							self.builder.get_object("vid4Spinbutton"),
							self.builder.get_object("vid5Spinbutton")
							]
		self.vidAdjustments = [
							self.builder.get_object("vid1Adjustment"),
							self.builder.get_object("vid2Adjustment"),
							self.builder.get_object("vid3Adjustment"),
							self.builder.get_object("vid4Adjustment"),
							self.builder.get_object("vid5Adjustment")
							]
		
		conn = self.__connect_cpu()
		frequencies = conn.GetFrequencies().split()
		defaultvids = conn.GetDefaultVids().split()
		currentvids = conn.GetCurrentVids().split()
		self.freqsnum = len(frequencies) # How many frequencies/vids we have?
		i = 0
		
		while i < self.freqsnum:
			self.freqLabels[i].set_text(frequencies[i] + " MHz")
			self.freqLabels[i].show()
			self.defaultVidLabels[i].set_text(defaultvids[i])
			self.defaultVidLabels[i].show()
			self.vidAdjustments[i].set_upper(int(defaultvids[i]))
			self.vidSpinbuttons[i].set_value(int(currentvids[i]))
			self.vidSpinbuttons[i].show()
			i += 1
		
	def __connect_cpu(self):
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_CPU)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		print unicode(_("Unable to connect to system service!"), "utf-8")
		sys.exit(1)
	
	def __connect_options(self):
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_OPTIONS)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		print unicode(_("Unable to connect to system service!"), "utf-8")
		sys.exit(1)
	
	def quit(self, widget = None, event = None):
		i = 0
		newvids = ""
		while i < self.freqsnum:
			newvids += str(self.vidSpinbuttons[i].get_value_as_int()) + " "
			i += 1
		newvids = newvids.strip()
		conn = self.__connect_cpu()
		if conn.GetCurrentVids() != newvids:
			title = unicode(_("Confirm"), "utf-8")
			message = unicode(_("Apply the new VIDs?"), "utf-8")
			dialog = gtk.MessageDialog(self.mainDialog, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION,
									gtk.BUTTONS_YES_NO, message)
			dialog.set_title(title)
			dialog.set_default_response(gtk.RESPONSE_NO)
			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				conn.SetCurrentVids(newvids)
		conn = self.__connect_options()
		if self.applyAtBootCheckbutton.get_active() == True:
			conn.SetPHCVids(newvids)
		else:
			conn.SetPHCVids("default")
			
		self.mainDialog.destroy()

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
		self.mainWindow.set_icon_from_file(SAMSUNG_TOOLS_ICON)
		self.mainWindow.connect("delete-event", self.quit)
		self.closeButton = self.builder.get_object("closeButton")
		self.closeButton.connect("clicked", self.quit)
		self.aboutButton = self.builder.get_object("aboutButton")
		self.aboutButton.connect("clicked", self.about)
	
		###
		### Session service configuration
		###
		self.sessionTable = self.builder.get_object("sessionTable")
		# Set backlight hotkey grabber
		self.backlightHotkeyButton = KeyGrabber(popup_title = unicode(_("Backlight"), "utf-8"))
		hotkey = session.GetBacklightHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.backlightHotkeyButton.set_label(key, mods, True)
		self.backlightHotkeyButton.set_tooltip_text(self.builder.get_object("backlightHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.backlightHotkeyButton, 1, 2, 2, 3, yoptions = 0)
		self.backlightHotkeyButton.connect("changed", self.on_backlightHotkeyButton_changed)
		self.backlightHotkeyButton.show()
		# Set bluetooth hotkey grabber
		self.bluetoothHotkeyButton = KeyGrabber(popup_title = unicode(_("Bluetooth"), "utf-8"))
		hotkey = session.GetBluetoothHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.bluetoothHotkeyButton.set_label(key, mods, True)
		self.bluetoothHotkeyButton.set_tooltip_text(self.builder.get_object("bluetoothHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.bluetoothHotkeyButton, 1, 2, 3, 4, yoptions = 0)
		self.bluetoothHotkeyButton.connect("changed", self.on_bluetoothHotkeyButton_changed)
		self.bluetoothHotkeyButton.show()
		# Set cpu hotkey grabber
		self.cpuHotkeyButton = KeyGrabber(popup_title = unicode(_("CPU fan"), "utf-8"))
		hotkey = session.GetCpuHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.cpuHotkeyButton.set_label(key, mods, True)
		self.cpuHotkeyButton.set_tooltip_text(self.builder.get_object("cpuHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.cpuHotkeyButton, 1, 2, 4, 5, yoptions = 0)
		self.cpuHotkeyButton.connect("changed", self.on_cpuHotkeyButton_changed)
		self.cpuHotkeyButton.show()
		# Set webcam hotkey grabber
		self.webcamHotkeyButton = KeyGrabber(popup_title = unicode(_("Webcam"), "utf-8"))
		hotkey = session.GetWebcamHotkey()
		(key, mods) = gtk.accelerator_parse(self.__convert_xbindkeys_to_gtk(hotkey))
		self.webcamHotkeyButton.set_label(key, mods, True)
		self.webcamHotkeyButton.set_tooltip_text(self.builder.get_object("webcamHotkeyLabel").get_tooltip_text())
		self.sessionTable.attach(self.webcamHotkeyButton, 1, 2, 5, 6, yoptions = 0)
		self.webcamHotkeyButton.connect("changed", self.on_webcamHotkeyButton_changed)
		self.webcamHotkeyButton.show()
		# Set wireless hotkey grabber
		self.wirelessHotkeyButton = KeyGrabber(popup_title = unicode(_("Wireless"), "utf-8"))
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
		### System service configuration
		###
		# Bluetooth initial status
		self.bluetoothInitialStatusCombobox = self.builder.get_object("bluetoothInitialStatusCombobox")
		# Set cell renderer for 'bluetooth initial status' combobox
		self.bluetoothInitialStatusComboboxCR = gtk.CellRendererText()
		self.bluetoothInitialStatusCombobox.pack_start(self.bluetoothInitialStatusComboboxCR)
		self.bluetoothInitialStatusCombobox.add_attribute(self.bluetoothInitialStatusComboboxCR, 'text', 0)
		status = system.GetBluetoothInitialStatus() 
		if status == "last":
			self.bluetoothInitialStatusCombobox.set_active(0)
		elif status == "on":
			self.bluetoothInitialStatusCombobox.set_active(1)
		else: # status == "off"
			self.bluetoothInitialStatusCombobox.set_active(2)
		self.bluetoothInitialStatusCombobox.connect("changed", self.on_bluetoothInitialStatusCombobox_changed)
		# Webcam initial status
		self.webcamInitialStatusCombobox = self.builder.get_object("webcamInitialStatusCombobox")
		# Set cell renderer for 'webcam initial status' combobox
		self.webcamInitialStatusComboboxCR = gtk.CellRendererText()
		self.webcamInitialStatusCombobox.pack_start(self.webcamInitialStatusComboboxCR)
		self.webcamInitialStatusCombobox.add_attribute(self.webcamInitialStatusComboboxCR, 'text', 0)
		status = system.GetWebcamInitialStatus()
		if status == "last":
			self.webcamInitialStatusCombobox.set_active(0)
		elif status == "on":
			self.webcamInitialStatusCombobox.set_active(1)
		else: # status == "off"
			self.webcamInitialStatusCombobox.set_active(2)
		self.webcamInitialStatusCombobox.connect("changed", self.on_webcamInitialStatusCombobox_changed)
		# Wireless initial status
		self.wirelessInitialStatusCombobox = self.builder.get_object("wirelessInitialStatusCombobox")
		# Set cell renderer for 'wireless initial status' combobox
		self.wirelessInitialStatusComboboxCR = gtk.CellRendererText()
		self.wirelessInitialStatusCombobox.pack_start(self.wirelessInitialStatusComboboxCR)
		self.wirelessInitialStatusCombobox.add_attribute(self.wirelessInitialStatusComboboxCR, 'text', 0)
		status = system.GetWirelessInitialStatus()
		if status == "last":
			self.wirelessInitialStatusCombobox.set_active(0)
		elif status == "on":
			self.wirelessInitialStatusCombobox.set_active(1)
		else: # status == "off"
			self.wirelessInitialStatusCombobox.set_active(2)
		self.wirelessInitialStatusCombobox.connect("changed", self.on_wirelessInitialStatusCombobox_changed)
		# CPU fan initial status
		self.cpufanInitialStatusCombobox = self.builder.get_object("cpufanInitialStatusCombobox")
		# Set cell renderer for 'cpufan initial status' combobox
		self.cpufanInitialStatusComboboxCR = gtk.CellRendererText()
		self.cpufanInitialStatusCombobox.pack_start(self.cpufanInitialStatusComboboxCR)
		self.cpufanInitialStatusCombobox.add_attribute(self.cpufanInitialStatusComboboxCR, 'text', 0)
		status = system.GetCpufanInitialStatus()
		if status == "normal":
			self.cpufanInitialStatusCombobox.set_active(0)
		elif status == "silent":
			self.cpufanInitialStatusCombobox.set_active(1)
		elif status == "speed":
			self.cpufanInitialStatusCombobox.set_active(2)
		else: # status == "last"
			self.cpufanInitialStatusCombobox.set_active(3)
		self.cpufanInitialStatusCombobox.connect("changed", self.on_cpufanInitialStatusCombobox_changed)
		# Set clean buttons
		self.bluetoothInitialStatusCleanButton = self.builder.get_object("bluetoothInitialStatusCleanButton")
		self.bluetoothInitialStatusCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.bluetoothInitialStatusCleanButton.connect("clicked", self.on_bluetoothInitialStatusCleanButton_clicked)
		self.webcamInitialStatusCleanButton = self.builder.get_object("webcamInitialStatusCleanButton")
		self.webcamInitialStatusCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.webcamInitialStatusCleanButton.connect("clicked", self.on_webcamInitialStatusCleanButton_clicked)
		self.wirelessInitialStatusCleanButton = self.builder.get_object("wirelessInitialStatusCleanButton")
		self.wirelessInitialStatusCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.wirelessInitialStatusCleanButton.connect("clicked", self.on_wirelessInitialStatusCleanButton_clicked)
		self.cpufanInitialStatusCleanButton = self.builder.get_object("cpufanInitialStatusCleanButton")
		self.cpufanInitialStatusCleanButton.set_image(gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
		self.cpufanInitialStatusCleanButton.connect("clicked", self.on_cpufanInitialStatusCleanButton_clicked)
		
		###
		### Advanced power management configuration
		###
		# kernel parameters
		self.sysCtlButton = self.builder.get_object("sysCtlButton")
		self.sysCtlButton.connect("clicked", self.on_sysCtlButton_clicked)
		# laptop mode tools
		self.laptopModeButton = self.builder.get_object("laptopModeButton")
		conn = self.__connect_system_laptopmode()
		if not conn.IsAvailable():
			self.laptopModeButton.set_sensitive(False)
			self.laptopModeButton.set_has_tooltip(True)
			tooltip = unicode(_("Install the 'laptop mode tools' package to configure these options"), "utf-8")
			self.laptopModeButton.set_tooltip_text(tooltip)
		else:
			self.laptopModeButton.set_sensitive(True)
		self.laptopModeButton.connect("clicked", self.on_laptopModeButton_clicked)
		# PHC
		self.phcButton = self.builder.get_object("phcButton")
		conn = self.__connect_system_cpu()
		if not conn.IsPHCAvailable():
			self.phcButton.set_sensitive(False)
			self.phcButton.set_has_tooltip(True)
			tooltip = unicode(_("You need a PHC enabled kernel to use this feature"), "utf-8")
			self.phcButton.set_tooltip_text(tooltip)
		else:
			self.phcButton.set_sensitive(True)
		self.phcButton.connect("clicked", self.on_phcButton_clicked)
		self.phcButton.show()
		
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
		print unicode(_("Unable to connect to session service!"), "utf-8")
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
		print unicode(_("Unable to connect to system service!"), "utf-8")
		sys.exit(1)
	
	def __connect_system_laptopmode(self):
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_LAPTOPMODE)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		print unicode(_("Unable to connect to system service!"), "utf-8")
		sys.exit(1)
	
	def __connect_system_cpu(self):
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_CPU)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		print unicode(_("Unable to connect to system service!"), "utf-8")
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
	
	def on_bluetoothInitialStatusCombobox_changed(self, combobox = None):
		system = self.__connect_system()
		active = combobox.get_active()
		if active == 0:
			system.SetBluetoothInitialStatus("last")
		elif active == 1:
			system.SetBluetoothInitialStatus("on")
		else:
			system.SetBluetoothInitialStatus("off")
			
	def on_webcamInitialStatusCombobox_changed(self, combobox = None):
		system = self.__connect_system()
		active = combobox.get_active()
		if active == 0:
			system.SetWebcamInitialStatus("last")
		elif active == 1:
			system.SetWebcamInitialStatus("on")
		else:
			system.SetWebcamInitialStatus("off")
	
	def on_wirelessInitialStatusCombobox_changed(self, combobox = None):
		system = self.__connect_system()
		active = combobox.get_active()
		if active == 0:
			system.SetWirelessInitialStatus("last")
		elif active == 1:
			system.SetWirelessInitialStatus("on")
		else:
			system.SetWirelessInitialStatus("off")
			
	def on_cpufanInitialStatusCombobox_changed(self, combobox = None):
		system = self.__connect_system()
		active = combobox.get_active()
		if active == 0:
			system.SetCpufanInitialStatus("normal")
		elif active == 1:
			system.SetCpufanInitialStatus("silent")
		elif active == 2:
			system.SetCpufanInitialStatus("speed")
		else:
			system.SetCpufanInitialStatus("last")
	
	def on_bluetoothInitialStatusCleanButton_clicked(self, button = None):
		if self.bluetoothInitialStatusCombobox.get_active() != 0:
			self.bluetoothInitialStatusCombobox.set_active(0)
	
	def on_webcamInitialStatusCleanButton_clicked(self, button = None):
		if self.webcamInitialStatusCombobox.get_active() != 0:
			self.webcamInitialStatusCombobox.set_active(0)
	
	def on_wirelessInitialStatusCleanButton_clicked(self, button = None):
		if self.wirelessInitialStatusCombobox.get_active() != 0:
			self.wirelessInitialStatusCombobox.set_active(0)
	
	def on_cpufanInitialStatusCleanButton_clicked(self, button = None):
		if self.cpufanInitialStatusCombobox.get_active() != 0:
			self.cpufanInitialStatusCombobox.set_active(0)
	
	def on_laptopModeButton_clicked(self, button):
		LaptopModeDialog(self.mainWindow)
	
	def on_sysCtlButton_clicked(self, button):
		KernelParametersDialog(self.mainWindow)
	
	def on_phcButton_clicked(self, button):
		title = unicode(_("Caution!"), "utf-8")
		message = unicode(_("CPU undervolting can lead to significant gains in terms of power energy saving, \
however <b>IT IS A RISKY PRACTICE</b> that might result in malfunctions \
and loss of data. Please be sure to know what you are doing, prior to use these options.\n\n\
Are you sure you want to continue?"), "utf-8")
		dialog = gtk.MessageDialog(self.mainWindow, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING,
								gtk.BUTTONS_YES_NO, None)
		dialog.set_title(title)
		dialog.set_markup(message)
		dialog.set_default_response(gtk.RESPONSE_NO)
		response = dialog.run()
		dialog.destroy()
		if response == gtk.RESPONSE_YES:
			PhcDialog(self.mainWindow)
	
	def about(self, button = None):
		authors = [ "Fortunato Ventre" ]
		artists = [ "http://icons.mysitemyway.com" ]
		translators = [
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
					"zeugma"
					]
		
		translators.sort(cmp = lambda x, y: cmp(x.lower(), y.lower()))
		
		dialog = gtk.AboutDialog()
		dialog.set_icon_from_file(SAMSUNG_TOOLS_ICON)
		dialog.set_name(APP_NAME)
		dialog.set_version(APP_VERSION)
		copyright = unicode(_("Released under GPLv3 license"), "utf-8") + "\n\nCopyleft by\nFortunato Ventre (voRia)\nvorione@gmail.com"
		dialog.set_copyright(copyright)
		dialog.set_website("http://www.voria.org/forum")
		dialog.set_website_label("Linux On My Samsung")
		dialog.set_authors(authors)
		dialog.set_artists(artists)
		temp = ""
		for name in translators:
			temp += name + "\n"
		dialog.set_translator_credits(temp)
		dialog.run()
		dialog.destroy()
	
	def quit(self, widget = None, event = None):
		gtk.main_quit()
	
if __name__ == "__main__":
	Main()
	gtk.main()
