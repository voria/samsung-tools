#!/usr/bin/python2
# coding=UTF-8
#
# Samsung-Tools
#
# Part of the 'Linux On My Samsung' project - <http://loms.voria.org>
#
# Copyleft (C) 2010 by
# Fortunato Ventre - <vorione@gmail.com> - <http://www.voria.org>
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
import dbus
import gettext
import sys

from backends.globals import *
from backends.session.util.icons import *

WORK_DIRECTORY = "/usr/share/samsung-tools"
sys.path.append(WORK_DIRECTORY)

_ = gettext.gettext
gettext.bindtextdomain("samsung-tools")
gettext.textdomain("samsung-tools")


class Popup (gtk.Window):
    # Popup (based on code from compizconfig-settings-manager)

    def __init__(self, text, title, parent=None):
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


class KeyGrabber(gtk.Button):
    # Key Grabber (based on code from compizconfig-settings-manager)
    __gsignals__ = {"changed": (gobject.SIGNAL_RUN_FIRST,
                                gobject.TYPE_NONE,
                                [gobject.TYPE_INT, gobject.TYPE_INT])}

    def __init__(self, label=None, popup_title=None):
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
        self.popup = Popup(_("Please press the new hotkey"),
                           self.popup_title, self)
        self.popup.show_all()
        self.handler = self.popup.connect(
            "key-press-event", self.on_key_press_event)
        while gtk.gdk.keyboard_grab(self.popup.window) != gtk.gdk.GRAB_SUCCESS:
            time.sleep(0.1)

    def end_key_grab(self):
        gtk.gdk.keyboard_ungrab(gtk.get_current_event_time())
        self.popup.disconnect(self.handler)
        self.popup.destroy()

    def on_key_press_event(self, widget, event):
        mods = event.state & gtk.accelerator_get_default_mod_mask()

        if event.keyval in (gtk.keysyms.Escape,
                            gtk.keysyms.Return) and not mods:
            self.end_key_grab()
            self.set_label(self.key, self.mods)
            return

        key = gtk.gdk.keyval_to_lower(event.keyval)
        if (key == gtk.keysyms.ISO_Left_Tab):
            key = gtk.keysyms.Tab

        if gtk.accelerator_valid(key, mods) or (
                key == gtk.keysyms.Tab and mods):
            self.set_label(key, mods, True)
            self.end_key_grab()
            return

        self.set_label(key, mods)

    def set_label(self, key=None, mods=None, valid=False):
        if key is not None and mods is not None:
            # emit 'changed' signal only when key is validated (valid = True)
            if valid:
                self.key = key
                self.mods = mods
                self.emit("changed", self.key, self.mods)
        if key is None and mods is None:
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
            if label == "XF86TouchpadToggle":
                label = "Fn-F10"
            label = label.replace("Primary", "Control")
        gtk.Button.set_label(self, label)


class KernelParametersDialog():

    def __init__(self, parent):
        # Setup GUI
        self.builder = gtk.Builder()
        self.builder.set_translation_domain("samsung-tools")
        self.builder.add_from_file(os.path.join(
            WORK_DIRECTORY, "gui/glade/samsung-tools-preferences-kernel-parameters.glade"))

        self.mainDialog = self.builder.get_object("mainDialog")
        self.mainDialog.set_icon_from_file(SAMSUNG_TOOLS_ICON)
        self.mainDialog.set_transient_for(parent)
        self.mainDialog.connect("delete-event", self.quit)

        self.closeButton = self.builder.get_object("closeButton")
        self.closeButton.connect("clicked", self.quit)

        # Swappiness
        conn = self.__connect()
        self.swappinessSpinbutton = self.builder.get_object(
            "swappinessSpinbutton")
        self.swappinessSpinbuttonValue = conn.GetSwappiness()
        self.swappinessSpinbutton.set_value(self.swappinessSpinbuttonValue)
        self.swappinessSpinbutton.connect(
            "value-changed", self.on_swappinessSpinbutton_valuechanged)

    def __connect(self):
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SystemBus()
                proxy = bus.get_object(
                    SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_SYSCTL)
                return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
            except:
                retry = retry - 1
        print unicode(_("Unable to connect to system service!"), "utf-8")
        sys.exit(1)

    def on_swappinessSpinbutton_valuechanged(self, button, event=None):
        self.swappinessSpinbuttonValue = button.get_value_as_int()
        # Value will be actually saved at the time the dialog is quitted

    def quit(self, widget=None, event=None):
        conn = self.__connect()
        conn.SetSwappiness(self.swappinessSpinbuttonValue)
        conn.ApplySettings()
        self.mainDialog.destroy()


class PowerManagementDialog():

    def __init__(self, parent):
        # Setup GUI
        self.builder = gtk.Builder()
        self.builder.set_translation_domain("samsung-tools")
        self.builder.add_from_file(os.path.join(
            WORK_DIRECTORY, "gui/glade/samsung-tools-preferences-power-management.glade"))

        self.mainDialog = self.builder.get_object("mainDialog")
        self.mainDialog.set_icon_from_file(SAMSUNG_TOOLS_ICON)
        self.mainDialog.set_transient_for(parent)
        self.mainDialog.connect("delete-event", self.quit)

        self.closeButton = self.builder.get_object("closeButton")
        self.closeButton.connect("clicked", self.quit)

        conn = self.__connect()

        # Devices Power Management
        self.devicesPowerManagement = self.builder.get_object(
            "devicesPowerManagement")
        self.devicesPowerManagement.set_sensitive(False)
        self.devicesPowerManagement.set_active(False)
        if conn.IsValid(PM_DEVICES_POWER_MANAGEMENT):
            self.devicesPowerManagement.set_sensitive(True)
            if conn.IsEnabled(PM_DEVICES_POWER_MANAGEMENT):
                self.devicesPowerManagement.set_active(True)
        self.devicesPowerManagement.connect(
            "toggled", self.on_devicesPowerManagement_toggled)

        # USB Autosuspend
        self.usbAutosuspend = self.builder.get_object("usbAutosuspend")
        self.usbAutosuspend.set_sensitive(False)
        self.usbAutosuspend.set_active(False)
        if conn.IsValid(PM_USB_AUTOSUSPEND):
            self.usbAutosuspend.set_sensitive(True)
            if conn.IsEnabled(PM_USB_AUTOSUSPEND):
                self.usbAutosuspend.set_active(True)
        self.usbAutosuspend.connect("toggled", self.on_usbAutosuspend_toggled)

        # VM Writeback Time
        self.vmWritebackTime = self.builder.get_object("vmWritebackTime")
        self.vmWritebackTime.set_sensitive(False)
        self.vmWritebackTime.set_active(False)
        if conn.IsValid(PM_VM_WRITEBACK_TIME):
            self.vmWritebackTime.set_sensitive(True)
            if conn.IsEnabled(PM_VM_WRITEBACK_TIME):
                self.vmWritebackTime.set_active(True)
        self.vmWritebackTime.connect(
            "toggled", self.on_vmWritebackTime_toggled)

    def __connect(self):
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SystemBus()
                proxy = bus.get_object(
                    SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_POWERMANAGEMENT)
                return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
            except:
                retry = retry - 1
        print unicode(_("Unable to connect to system service!"), "utf-8")
        sys.exit(1)

    def on_devicesPowerManagement_toggled(self, button=None):
        conn = self.__connect()
        conn.Toggle(PM_DEVICES_POWER_MANAGEMENT)

    def on_usbAutosuspend_toggled(self, button=None):
        conn = self.__connect()
        conn.Toggle(PM_USB_AUTOSUSPEND)

    def on_vmWritebackTime_toggled(self, button=None):
        conn = self.__connect()
        conn.Toggle(PM_VM_WRITEBACK_TIME)

    def quit(self, widget=None, event=None):
        self.mainDialog.destroy()


class PhcDialog():

    def __init__(self, parent):
        # Setup GUI
        self.builder = gtk.Builder()
        self.builder.set_translation_domain("samsung-tools")
        self.builder.add_from_file(os.path.join(
            WORK_DIRECTORY, "gui/glade/samsung-tools-preferences-phc.glade"))

        self.mainDialog = self.builder.get_object("mainDialog")
        self.mainDialog.set_icon_from_file(SAMSUNG_TOOLS_ICON)
        self.mainDialog.set_transient_for(parent)
        self.mainDialog.connect("delete-event", self.quit)

        self.closeButton = self.builder.get_object("closeButton")
        self.closeButton.connect("clicked", self.quit)

        self.applyAtBootCheckbutton = self.builder.get_object(
            "applyAtBootCheckbutton")
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
        self.freqsnum = len(frequencies)  # How many frequencies/vids we have?
        minvid = int(defaultvids[self.freqsnum - 1])
        i = 0
        while i < self.freqsnum:
            self.freqLabels[i].set_text(frequencies[i] + " MHz")
            self.freqLabels[i].show()
            self.defaultVidLabels[i].set_text(defaultvids[i])
            self.defaultVidLabels[i].show()
            self.vidAdjustments[i].set_lower(minvid)
            self.vidAdjustments[i].set_upper(int(defaultvids[i]))
            self.vidSpinbuttons[i].set_value(int(currentvids[i]))
            self.vidSpinbuttons[i].show()
            i += 1

    def __connect_cpu(self):
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SystemBus()
                proxy = bus.get_object(
                    SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_CPU)
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
                proxy = bus.get_object(
                    SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_OPTIONS)
                return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
            except:
                retry = retry - 1
        print unicode(_("Unable to connect to system service!"), "utf-8")
        sys.exit(1)

    def quit(self, widget=None, event=None):
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
        if self.applyAtBootCheckbutton.get_active():
            conn.SetPHCVids(newvids)
        else:
            conn.SetPHCVids("default")

        self.mainDialog.destroy()


class Main():

    def __init__(self):
        # Get interfaces for D-Bus services
        session = self.__connect_session_options()
        system = self.__connect_system_options()

        # Setup GUI
        self.builder = gtk.Builder()
        self.builder.set_translation_domain("samsung-tools")
        self.builder.add_from_file(os.path.join(
            WORK_DIRECTORY, "gui/glade/samsung-tools-preferences.glade"))

        ###
        # Main widgets
        ###
        self.mainWindow = self.builder.get_object("mainWindow")
        self.mainWindow.set_icon_from_file(SAMSUNG_TOOLS_ICON)
        self.mainWindow.connect("delete-event", self.quit)
        self.closeButton = self.builder.get_object("closeButton")
        self.closeButton.connect("clicked", self.quit)
        self.aboutButton = self.builder.get_object("aboutButton")
        self.aboutButton.connect("clicked", self.about)

        ###
        # Session service configuration
        ###
        self.sessionTable = self.builder.get_object("sessionTable")
        # Set backlight hotkey grabber
        self.backlightHotkeyButton = KeyGrabber(
            popup_title=unicode(_("Backlight"), "utf-8"))
        hotkey = session.GetBacklightHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.backlightHotkeyButton.set_label(key, mods, True)
        self.backlightHotkeyButton.set_tooltip_text(
            self.builder.get_object("backlightHotkeyLabel").get_tooltip_text())
        self.sessionTable.attach(
            self.backlightHotkeyButton, 1, 2, 2, 3, yoptions=0)
        self.backlightHotkeyButton.connect(
            "changed", self.on_backlightHotkeyButton_changed)
        self.backlightHotkeyButton.show()
        # Set bluetooth hotkey grabber
        self.bluetoothHotkeyButton = KeyGrabber(
            popup_title=unicode(_("Bluetooth"), "utf-8"))
        hotkey = session.GetBluetoothHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.bluetoothHotkeyButton.set_label(key, mods, True)
        self.bluetoothHotkeyButton.set_tooltip_text(
            self.builder.get_object("bluetoothHotkeyLabel").get_tooltip_text())
        self.sessionTable.attach(
            self.bluetoothHotkeyButton, 1, 2, 3, 4, yoptions=0)
        self.bluetoothHotkeyButton.connect(
            "changed", self.on_bluetoothHotkeyButton_changed)
        self.bluetoothHotkeyButton.show()
        # Set cpu hotkey grabber
        self.cpuHotkeyButton = KeyGrabber(
            popup_title=unicode(_("CPU fan"), "utf-8"))
        hotkey = session.GetCpuHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.cpuHotkeyButton.set_label(key, mods, True)
        self.cpuHotkeyButton.set_tooltip_text(
            self.builder.get_object("cpuHotkeyLabel").get_tooltip_text())
        self.sessionTable.attach(self.cpuHotkeyButton, 1, 2, 4, 5, yoptions=0)
        self.cpuHotkeyButton.connect(
            "changed", self.on_cpuHotkeyButton_changed)
        self.cpuHotkeyButton.show()
        # Set webcam hotkey grabber
        self.webcamHotkeyButton = KeyGrabber(
            popup_title=unicode(_("Webcam"), "utf-8"))
        hotkey = session.GetWebcamHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.webcamHotkeyButton.set_label(key, mods, True)
        self.webcamHotkeyButton.set_tooltip_text(
            self.builder.get_object("webcamHotkeyLabel").get_tooltip_text())
        self.sessionTable.attach(
            self.webcamHotkeyButton, 1, 2, 5, 6, yoptions=0)
        self.webcamHotkeyButton.connect(
            "changed", self.on_webcamHotkeyButton_changed)
        self.webcamHotkeyButton.show()
        # Set wireless hotkey grabber
        self.wirelessHotkeyButton = KeyGrabber(
            popup_title=unicode(_("Wireless"), "utf-8"))
        hotkey = session.GetWirelessHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.wirelessHotkeyButton.set_label(key, mods, True)
        self.wirelessHotkeyButton.set_tooltip_text(
            self.builder.get_object("wirelessHotkeyLabel").get_tooltip_text())
        self.sessionTable.attach(
            self.wirelessHotkeyButton, 1, 2, 6, 7, yoptions=0)
        self.wirelessHotkeyButton.connect(
            "changed", self.on_wirelessHotkeyButton_changed)
        self.wirelessHotkeyButton.show()
        # Set clean buttons for keygrabbers
        self.backlightHotkeyCleanButton = self.builder.get_object(
            "backlightHotkeyCleanButton")
        self.backlightHotkeyCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
        self.backlightHotkeyCleanButton.connect(
            "clicked", self.on_backlightHotkeyCleanButton_clicked)
        self.bluetoothHotkeyCleanButton = self.builder.get_object(
            "bluetoothHotkeyCleanButton")
        self.bluetoothHotkeyCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
        self.bluetoothHotkeyCleanButton.connect(
            "clicked", self.on_bluetoothHotkeyCleanButton_clicked)
        self.cpuHotkeyCleanButton = self.builder.get_object(
            "cpuHotkeyCleanButton")
        self.cpuHotkeyCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
        self.cpuHotkeyCleanButton.connect(
            "clicked", self.on_cpuHotkeyCleanButton_clicked)
        self.webcamHotkeyCleanButton = self.builder.get_object(
            "webcamHotkeyCleanButton")
        self.webcamHotkeyCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
        self.webcamHotkeyCleanButton.connect(
            "clicked", self.on_webcamHotkeyCleanButton_clicked)
        self.wirelessHotkeyCleanButton = self.builder.get_object(
            "wirelessHotkeyCleanButton")
        self.wirelessHotkeyCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU))
        self.wirelessHotkeyCleanButton.connect(
            "clicked", self.on_wirelessHotkeyCleanButton_clicked)
        # Set default buttons for keygrabbers
        self.backlightHotkeyDefaultButton = self.builder.get_object(
            "backlightHotkeyDefaultButton")
        self.backlightHotkeyDefaultButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.backlightHotkeyDefaultButton.connect(
            "clicked", self.on_backlightHotkeyDefaultButton_clicked)
        self.bluetoothHotkeyDefaultButton = self.builder.get_object(
            "bluetoothHotkeyDefaultButton")
        self.bluetoothHotkeyDefaultButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.bluetoothHotkeyDefaultButton.connect(
            "clicked", self.on_bluetoothHotkeyDefaultButton_clicked)
        self.cpuHotkeyDefaultButton = self.builder.get_object(
            "cpuHotkeyDefaultButton")
        self.cpuHotkeyDefaultButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.cpuHotkeyDefaultButton.connect(
            "clicked", self.on_cpuHotkeyDefaultButton_clicked)
        self.webcamHotkeyDefaultButton = self.builder.get_object(
            "webcamHotkeyDefaultButton")
        self.webcamHotkeyDefaultButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.webcamHotkeyDefaultButton.connect(
            "clicked", self.on_webcamHotkeyDefaultButton_clicked)
        self.wirelessHotkeyDefaultButton = self.builder.get_object(
            "wirelessHotkeyDefaultButton")
        self.wirelessHotkeyDefaultButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.wirelessHotkeyDefaultButton.connect(
            "clicked", self.on_wirelessHotkeyDefaultButton_clicked)
        # Set enable hotkeys checkbutton
        self.backlightHotkeyLabel = self.builder.get_object(
            "backlightHotkeyLabel")
        self.bluetoothHotkeyLabel = self.builder.get_object(
            "bluetoothHotkeyLabel")
        self.cpuHotkeyLabel = self.builder.get_object("cpuHotkeyLabel")
        self.webcamHotkeyLabel = self.builder.get_object("webcamHotkeyLabel")
        self.wirelessHotkeyLabel = self.builder.get_object(
            "wirelessHotkeyLabel")
        self.useHotkeysCheckbutton = self.builder.get_object(
            "useHotkeysCheckbutton")
        if session.GetUseHotkeys() == "true":
            self.useHotkeysCheckbutton.set_active(True)
        else:
            self.useHotkeysCheckbutton.set_active(False)
        self.useHotkeysCheckbutton.connect(
            "toggled", self.on_useHotkeysCheckbutton_toggled)
        self.on_useHotkeysCheckbutton_toggled(self.useHotkeysCheckbutton, True)

        ###
        # System service configuration
        ###
        # Bluetooth initial status
        self.bluetoothInitialStatusCombobox = self.builder.get_object(
            "bluetoothInitialStatusCombobox")
        # Set cell renderer for 'bluetooth initial status' combobox
        self.bluetoothInitialStatusComboboxCR = gtk.CellRendererText()
        self.bluetoothInitialStatusCombobox.pack_start(
            self.bluetoothInitialStatusComboboxCR)
        self.bluetoothInitialStatusCombobox.add_attribute(
            self.bluetoothInitialStatusComboboxCR, 'text', 0)
        status = system.GetBluetoothInitialStatus()
        if status == "last":
            self.bluetoothInitialStatusCombobox.set_active(0)
        elif status == "on":
            self.bluetoothInitialStatusCombobox.set_active(1)
        else:  # status == "off"
            self.bluetoothInitialStatusCombobox.set_active(2)
        self.bluetoothInitialStatusCombobox.connect(
            "changed", self.on_bluetoothInitialStatusCombobox_changed)
        # Webcam initial status
        self.webcamInitialStatusCombobox = self.builder.get_object(
            "webcamInitialStatusCombobox")
        # Set cell renderer for 'webcam initial status' combobox
        self.webcamInitialStatusComboboxCR = gtk.CellRendererText()
        self.webcamInitialStatusCombobox.pack_start(
            self.webcamInitialStatusComboboxCR)
        self.webcamInitialStatusCombobox.add_attribute(
            self.webcamInitialStatusComboboxCR, 'text', 0)
        status = system.GetWebcamInitialStatus()
        if status == "last":
            self.webcamInitialStatusCombobox.set_active(0)
        elif status == "on":
            self.webcamInitialStatusCombobox.set_active(1)
        else:  # status == "off"
            self.webcamInitialStatusCombobox.set_active(2)
        self.webcamInitialStatusCombobox.connect(
            "changed", self.on_webcamInitialStatusCombobox_changed)
        # Wireless initial status
        self.wirelessInitialStatusCombobox = self.builder.get_object(
            "wirelessInitialStatusCombobox")
        # Set cell renderer for 'wireless initial status' combobox
        self.wirelessInitialStatusComboboxCR = gtk.CellRendererText()
        self.wirelessInitialStatusCombobox.pack_start(
            self.wirelessInitialStatusComboboxCR)
        self.wirelessInitialStatusCombobox.add_attribute(
            self.wirelessInitialStatusComboboxCR, 'text', 0)
        status = system.GetWirelessInitialStatus()
        if status == "last":
            self.wirelessInitialStatusCombobox.set_active(0)
        elif status == "on":
            self.wirelessInitialStatusCombobox.set_active(1)
        else:  # status == "off"
            self.wirelessInitialStatusCombobox.set_active(2)
        self.wirelessInitialStatusCombobox.connect(
            "changed", self.on_wirelessInitialStatusCombobox_changed)
        # CPU fan initial status
        self.cpufanInitialStatusCombobox = self.builder.get_object(
            "cpufanInitialStatusCombobox")
        # Set cell renderer for 'cpufan initial status' combobox
        self.cpufanInitialStatusComboboxCR = gtk.CellRendererText()
        self.cpufanInitialStatusCombobox.pack_start(
            self.cpufanInitialStatusComboboxCR)
        self.cpufanInitialStatusCombobox.add_attribute(
            self.cpufanInitialStatusComboboxCR, 'text', 0)
        status = system.GetCpufanInitialStatus()
        if status == "normal":
            self.cpufanInitialStatusCombobox.set_active(0)
        elif status == "silent":
            self.cpufanInitialStatusCombobox.set_active(1)
        elif status == "overclock":
            self.cpufanInitialStatusCombobox.set_active(2)
        else:  # status == "last"
            self.cpufanInitialStatusCombobox.set_active(3)
        self.cpufanInitialStatusCombobox.connect(
            "changed", self.on_cpufanInitialStatusCombobox_changed)
        # Set clean buttons
        self.bluetoothInitialStatusCleanButton = self.builder.get_object(
            "bluetoothInitialStatusCleanButton")
        self.bluetoothInitialStatusCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.bluetoothInitialStatusCleanButton.connect(
            "clicked", self.on_bluetoothInitialStatusCleanButton_clicked)
        self.webcamInitialStatusCleanButton = self.builder.get_object(
            "webcamInitialStatusCleanButton")
        self.webcamInitialStatusCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.webcamInitialStatusCleanButton.connect(
            "clicked", self.on_webcamInitialStatusCleanButton_clicked)
        self.wirelessInitialStatusCleanButton = self.builder.get_object(
            "wirelessInitialStatusCleanButton")
        self.wirelessInitialStatusCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.wirelessInitialStatusCleanButton.connect(
            "clicked", self.on_wirelessInitialStatusCleanButton_clicked)
        self.cpufanInitialStatusCleanButton = self.builder.get_object(
            "cpufanInitialStatusCleanButton")
        self.cpufanInitialStatusCleanButton.set_image(
            gtk.image_new_from_stock(gtk.STOCK_CLEAR, gtk.ICON_SIZE_MENU))
        self.cpufanInitialStatusCleanButton.connect(
            "clicked", self.on_cpufanInitialStatusCleanButton_clicked)
        # Disable widgets for devices not available
        # Get remaining widgets
        self.bluetoothInitialStatusLabel = self.builder.get_object(
            "bluetoothInitialStatusLabel")
        self.webcamInitialStatusLabel = self.builder.get_object(
            "webcamInitialStatusLabel")
        self.wirelessInitialStatusLabel = self.builder.get_object(
            "wirelessInitialStatusLabel")
        self.cpufanInitialStatusLabel = self.builder.get_object(
            "cpufanInitialStatusLabel")
        conn = self.__connect_session_bluetooth()
        if not conn.IsAvailable():
            self.bluetoothInitialStatusLabel.set_sensitive(False)
            self.bluetoothInitialStatusCombobox.set_sensitive(False)
            self.bluetoothInitialStatusCleanButton.set_sensitive(False)
        conn = self.__connect_session_webcam()
        if not conn.IsAvailable():
            self.webcamInitialStatusLabel.set_sensitive(False)
            self.webcamInitialStatusCombobox.set_sensitive(False)
            self.webcamInitialStatusCleanButton.set_sensitive(False)
        conn = self.__connect_session_wireless()
        if not conn.IsAvailable():
            self.wirelessInitialStatusLabel.set_sensitive(False)
            self.wirelessInitialStatusCombobox.set_sensitive(False)
            self.wirelessInitialStatusCleanButton.set_sensitive(False)
        conn = self.__connect_session_cpu()
        if not conn.IsFanAvailable():
            self.cpufanInitialStatusLabel.set_sensitive(False)
            self.cpufanInitialStatusCombobox.set_sensitive(False)
            self.cpufanInitialStatusCleanButton.set_sensitive(False)
        # Set control interface
        self.controlInterfaceValueLabel = self.builder.get_object(
            "controlInterfaceValueLabel")
        ci = system.GetControlInterface()
        if ci == "esdm":
            self.controlInterfaceValueLabel.set_label("easy-slow-down-manager")
        elif ci == "sl":
            self.controlInterfaceValueLabel.set_label("samsung-laptop")
        else:
            self.controlInterfaceValueLabel.set_label("-")

        ###
        # Advanced power management configuration
        ###
        # Kernel parameters
        self.sysCtlButton = self.builder.get_object("sysCtlButton")
        conn = self.__connect_system_sysctl()
        if not conn.IsAvailable():
            self.sysCtlButton.set_sensitive(False)
        else:
            self.sysCtlButton.set_sensitive(True)
            self.sysCtlButton.connect("clicked", self.on_sysCtlButton_clicked)
        # Power management
        self.powerManagementButton = self.builder.get_object(
            "powerManagementButton")
        self.powerManagementButton.set_sensitive(True)
        self.powerManagementButton.connect(
            "clicked", self.on_powerManagementButton_clicked)
        # PHC
        self.phcButton = self.builder.get_object("phcButton")
        conn = self.__connect_system_cpu()
        if not conn.IsPHCAvailable():
            self.phcButton.set_sensitive(False)
            self.phcButton.set_has_tooltip(True)
            tooltip = unicode(
                _("You need a PHC enabled kernel to use this feature"), "utf-8")
            self.phcButton.set_tooltip_text(tooltip)
        else:
            self.phcButton.set_sensitive(True)
        self.phcButton.connect("clicked", self.on_phcButton_clicked)

        # Enable click on website url in about dialog
        def about_dialog_url_clicked(dialog, link, user_data):
            import webbrowser
            webbrowser.open(link)
        gtk.about_dialog_set_url_hook(about_dialog_url_clicked, None)

        # All ready
        self.mainWindow.show()

    def __connect_session_options(self):
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_OPTIONS)
                return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
            except:
                retry = retry - 1
        print unicode(_("Unable to connect to session service!"), "utf-8")
        sys.exit(1)

    def __connect_session_bluetooth(self):
        """ Connect to session service for bluetooth control """
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_BLUETOOTH)
                return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
            except:
                retry = retry - 1
        sys.exit(1)

    def __connect_session_webcam(self):
        """ Connect to session service for webcam control """
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_WEBCAM)
                return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
            except:
                retry = retry - 1
        sys.exit(1)

    def __connect_session_wireless(self):
        """ Connect to session service for wireless control """
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_WIRELESS)
                return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
            except:
                retry = retry - 1
        sys.exit(1)

    def __connect_session_cpu(self):
        """ Connect to session service for cpu fan control """
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME, SESSION_OBJECT_PATH_CPU)
                return dbus.Interface(proxy, SESSION_INTERFACE_NAME)
            except:
                retry = retry - 1
        sys.exit(1)

    def __connect_system_options(self):
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SystemBus()
                proxy = bus.get_object(
                    SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_OPTIONS)
                return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
            except:
                retry = retry - 1
        print unicode(_("Unable to connect to system service!"), "utf-8")
        sys.exit(1)

    def __connect_system_sysctl(self):
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SystemBus()
                proxy = bus.get_object(
                    SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_SYSCTL)
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
                proxy = bus.get_object(
                    SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_CPU)
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
            if key == "Primary":
                key = "Control"
            result += key + "+"
        result = result[0:len(result) - 1]  # Remove the '+' at the end
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

    def __set_backlight_hotkey_sensitiveness(self, active):
        self.backlightHotkeyLabel.set_sensitive(active)
        self.backlightHotkeyButton.set_sensitive(active)
        self.backlightHotkeyCleanButton.set_sensitive(active)
        self.backlightHotkeyDefaultButton.set_sensitive(active)

    def __set_bluetooth_hotkey_sensitiveness(self, active):
        # Check if bluetooth is actually available
        conn = self.__connect_session_bluetooth()
        if not conn.IsAvailable():
            # Not available, disable the hotkey
            self.bluetoothHotkeyButton.set_label(0, 0, True)
            # Disable the widgets
            active = False
        self.bluetoothHotkeyLabel.set_sensitive(active)
        self.bluetoothHotkeyButton.set_sensitive(active)
        self.bluetoothHotkeyCleanButton.set_sensitive(active)
        self.bluetoothHotkeyDefaultButton.set_sensitive(active)

    def __set_cpu_hotkey_sensitiveness(self, active):
        # Check if cpu fan control is actually available
        conn = self.__connect_session_cpu()
        if not conn.IsFanAvailable():
            # Not available, disable the hotkey
            self.cpuHotkeyButton.set_label(0, 0, True)
            # Disable the widgets
            active = False
        self.cpuHotkeyLabel.set_sensitive(active)
        self.cpuHotkeyButton.set_sensitive(active)
        self.cpuHotkeyCleanButton.set_sensitive(active)
        self.cpuHotkeyDefaultButton.set_sensitive(active)

    def __set_webcam_hotkey_sensitiveness(self, active):
        # Check if webcam is actually available
        conn = self.__connect_session_webcam()
        if not conn.IsAvailable():
            # Not available, disable the hotkey
            self.webcamHotkeyButton.set_label(0, 0, True)
            # Disable the widgets
            active = False
        self.webcamHotkeyLabel.set_sensitive(active)
        self.webcamHotkeyButton.set_sensitive(active)
        self.webcamHotkeyCleanButton.set_sensitive(active)
        self.webcamHotkeyDefaultButton.set_sensitive(active)

    def __set_wireless_hotkey_sensitiveness(self, active):
        # Check if wireless is actually available
        conn = self.__connect_session_wireless()
        if not conn.IsAvailable():
            # Not available, disable the hotkey
            self.wirelessHotkeyButton.set_label(0, 0, True)
            # Disable the widgets
            active = False
        self.wirelessHotkeyLabel.set_sensitive(active)
        self.wirelessHotkeyButton.set_sensitive(active)
        self.wirelessHotkeyCleanButton.set_sensitive(active)
        self.wirelessHotkeyDefaultButton.set_sensitive(active)

    def on_useHotkeysCheckbutton_toggled(
            self, checkbutton=None, toggle_widgets_only=False):
        self.__set_backlight_hotkey_sensitiveness(checkbutton.get_active())
        self.__set_bluetooth_hotkey_sensitiveness(checkbutton.get_active())
        self.__set_cpu_hotkey_sensitiveness(checkbutton.get_active())
        self.__set_webcam_hotkey_sensitiveness(checkbutton.get_active())
        self.__set_wireless_hotkey_sensitiveness(checkbutton.get_active())

        if not toggle_widgets_only:
            session = self.__connect_session_options()
            if checkbutton.get_active():
                session.SetUseHotkeys("true")
            else:
                session.SetUseHotkeys("false")

    def on_backlightHotkeyButton_changed(
            self, button=None, key=None, mods=None):
        if key == 0 and mods == 0:
            new = "disable"
        else:
            new = gtk.accelerator_name(key, mods)
        session = self.__connect_session_options()
        session.SetBacklightHotkey(self.__convert_gtk_to_xbindkeys(new))

    def on_bluetoothHotkeyButton_changed(
            self, button=None, key=None, mods=None):
        if key == 0 and mods == 0:
            new = "disable"
        else:
            new = gtk.accelerator_name(key, mods)
        session = self.__connect_session_options()
        session.SetBluetoothHotkey(self.__convert_gtk_to_xbindkeys(new))

    def on_cpuHotkeyButton_changed(self, button=None, key=None, mods=None):
        if key == 0 and mods == 0:
            new = "disable"
        else:
            new = gtk.accelerator_name(key, mods)
        session = self.__connect_session_options()
        session.SetCpuHotkey(self.__convert_gtk_to_xbindkeys(new))

    def on_webcamHotkeyButton_changed(self, button=None, key=None, mods=None):
        if key == 0 and mods == 0:
            new = "disable"
        else:
            new = gtk.accelerator_name(key, mods)
        session = self.__connect_session_options()
        session.SetWebcamHotkey(self.__convert_gtk_to_xbindkeys(new))

    def on_wirelessHotkeyButton_changed(
            self, button=None, key=None, mods=None):
        if key == 0 and mods == 0:
            new = "disable"
        else:
            new = gtk.accelerator_name(key, mods)
        session = self.__connect_session_options()
        session.SetWirelessHotkey(self.__convert_gtk_to_xbindkeys(new))

    def on_backlightHotkeyCleanButton_clicked(self, button=None):
        self.backlightHotkeyButton.set_label(0, 0, True)

    def on_bluetoothHotkeyCleanButton_clicked(self, button=None):
        self.bluetoothHotkeyButton.set_label(0, 0, True)

    def on_cpuHotkeyCleanButton_clicked(self, button=None):
        self.cpuHotkeyButton.set_label(0, 0, True)

    def on_webcamHotkeyCleanButton_clicked(self, button=None):
        self.webcamHotkeyButton.set_label(0, 0, True)

    def on_wirelessHotkeyCleanButton_clicked(self, button=None):
        self.wirelessHotkeyButton.set_label(0, 0, True)

    def on_backlightHotkeyDefaultButton_clicked(self, button=None):
        session = self.__connect_session_options()
        session.SetBacklightHotkey("default")
        hotkey = session.GetBacklightHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.backlightHotkeyButton.set_label(key, mods, True)

    def on_bluetoothHotkeyDefaultButton_clicked(self, button=None):
        session = self.__connect_session_options()
        session.SetBluetoothHotkey("default")
        hotkey = session.GetBluetoothHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.bluetoothHotkeyButton.set_label(key, mods, True)

    def on_cpuHotkeyDefaultButton_clicked(self, button=None):
        session = self.__connect_session_options()
        session.SetCpuHotkey("default")
        hotkey = session.GetCpuHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.cpuHotkeyButton.set_label(key, mods, True)

    def on_webcamHotkeyDefaultButton_clicked(self, button=None):
        session = self.__connect_session_options()
        session.SetWebcamHotkey("default")
        hotkey = session.GetWebcamHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.webcamHotkeyButton.set_label(key, mods, True)

    def on_wirelessHotkeyDefaultButton_clicked(self, button=None):
        session = self.__connect_session_options()
        session.SetWirelessHotkey("default")
        hotkey = session.GetWirelessHotkey()
        (key, mods) = gtk.accelerator_parse(
            self.__convert_xbindkeys_to_gtk(hotkey))
        self.wirelessHotkeyButton.set_label(key, mods, True)

    def on_bluetoothInitialStatusCombobox_changed(self, combobox=None):
        system = self.__connect_system_options()
        active = combobox.get_active()
        if active == 0:
            system.SetBluetoothInitialStatus("last")
        elif active == 1:
            system.SetBluetoothInitialStatus("on")
        else:
            system.SetBluetoothInitialStatus("off")

    def on_webcamInitialStatusCombobox_changed(self, combobox=None):
        system = self.__connect_system_options()
        active = combobox.get_active()
        if active == 0:
            system.SetWebcamInitialStatus("last")
        elif active == 1:
            system.SetWebcamInitialStatus("on")
        else:
            system.SetWebcamInitialStatus("off")

    def on_wirelessInitialStatusCombobox_changed(self, combobox=None):
        system = self.__connect_system_options()
        active = combobox.get_active()
        if active == 0:
            system.SetWirelessInitialStatus("last")
        elif active == 1:
            system.SetWirelessInitialStatus("on")
        else:
            system.SetWirelessInitialStatus("off")

    def on_cpufanInitialStatusCombobox_changed(self, combobox=None):
        system = self.__connect_system_options()
        active = combobox.get_active()
        if active == 0:
            system.SetCpufanInitialStatus("normal")
        elif active == 1:
            system.SetCpufanInitialStatus("silent")
        elif active == 2:
            system.SetCpufanInitialStatus("overclock")
        else:
            system.SetCpufanInitialStatus("last")

    def on_bluetoothInitialStatusCleanButton_clicked(self, button=None):
        if self.bluetoothInitialStatusCombobox.get_active() != 0:
            self.bluetoothInitialStatusCombobox.set_active(0)

    def on_webcamInitialStatusCleanButton_clicked(self, button=None):
        if self.webcamInitialStatusCombobox.get_active() != 0:
            self.webcamInitialStatusCombobox.set_active(0)

    def on_wirelessInitialStatusCleanButton_clicked(self, button=None):
        if self.wirelessInitialStatusCombobox.get_active() != 0:
            self.wirelessInitialStatusCombobox.set_active(0)

    def on_cpufanInitialStatusCleanButton_clicked(self, button=None):
        if self.cpufanInitialStatusCombobox.get_active() != 0:
            self.cpufanInitialStatusCombobox.set_active(0)

    def on_sysCtlButton_clicked(self, button):
        KernelParametersDialog(self.mainWindow)

    def on_powerManagementButton_clicked(self, button):
        PowerManagementDialog(self.mainWindow)

    def on_phcButton_clicked(self, button):
        title = unicode(_("Caution!"), "utf-8")
        message = unicode(_("CPU undervolting can lead to significant gains in terms of power energy saving, \
however <b>IT IS A RISKY PRACTICE</b> that might result in malfunctions \
and loss of data. Please be sure to know what you are doing, prior to use these options.\n\n\
Are you sure you want to continue?"), "utf-8")
        dialog = gtk.MessageDialog(
            self.mainWindow, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, None)
        dialog.set_title(title)
        dialog.set_markup(message)
        dialog.set_default_response(gtk.RESPONSE_NO)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            PhcDialog(self.mainWindow)

    def about(self, button=None):
        ARTISTS_LIST.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))
        TRANSLATORS_LIST.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))

        dialog = gtk.AboutDialog()
        dialog.set_icon_from_file(SAMSUNG_TOOLS_ICON)
        dialog.set_name(APP_NAME)
        dialog.set_version(APP_VERSION)
        copyright = unicode(_("Released under GPLv3 license"), "utf-8") + \
            "\n\nCopyleft by\nFortunato Ventre\nvorione@gmail.com"
        dialog.set_copyright(copyright)
        dialog.set_website("http://loms.voria.org")
        dialog.set_website_label("Linux On My Samsung")
        dialog.set_authors(AUTHORS_LIST)
        dialog.set_artists(ARTISTS_LIST)
        translators = ""
        for name in TRANSLATORS_LIST:
            translators += name + "\n"
        dialog.set_translator_credits(translators)
        dialog.run()
        dialog.destroy()

    def quit(self, widget=None, event=None):
        gtk.main_quit()

if __name__ == "__main__":
    Main()
    gtk.main()
