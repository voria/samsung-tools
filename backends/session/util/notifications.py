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

import subprocess
from backends.globals import *

# Try to use these notification methods, in order:
# "pynotify" - Use pynotify module (notify-osd / gnome)
# "dbus" - Use "org.freedesktop.Notifications" interface through dbus (kde)
# None - Do not use notification system
try:
    method = None
    command = "ps x"
    process = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output = process.communicate()[0]
    if output.find("gnome-session") != -1:
        method = "pynotify"
        import pynotify
    if method is None:
        raise
except:
    method = "dbus"

import dbus
DBUS_METHOD_INTERFACE = "org.freedesktop.Notifications"
DBUS_METHOD_OBJECT = "/org/freedesktop/Notifications"


class Notification():
    """ Show user's notifications. """

    def __init__(self, title=None, message=None, icon=None, urgency="normal"):
        self.initialized = False  # Is notification system initialized
        global method
        if method == "pynotify":
            if pynotify.init("Samsung-Tools Notification System"):
                # Create a new notification
                self.notify = pynotify.Notification(" ")
                # Set initial values
                self.setTitle(title)
                self.setMessage(message)
                self.setIcon(icon)
                self.setUrgency(urgency)
                self.initialized = True
            else:
                sessionlog.write(
                    "ERROR: 'Notification' - cannot use 'pynotify' method. Trying with 'dbus' one.")
                method = "dbus"
        if method == "dbus":
            if self.__connect() is not None:
                self.initialized = True
            else:
                method = None
        # Set a default timeout
        self.timeout = 5000

    def __connect(self):
        """ Enable connection to session backend (used when method == 'dbus'). """
        retry = 3
        while retry > 0:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    DBUS_METHOD_INTERFACE, DBUS_METHOD_OBJECT)
                return dbus.Interface(proxy, DBUS_METHOD_INTERFACE)
            except:
                retry = retry - 1
        return None

    def setTitle(self, title):
        """ Set notification's title. """
        self.title = title

    def setMessage(self, message):
        """ Set notification's message. """
        self.message = message

    def setIcon(self, icon):
        """ Set notification's icon. """
        self.icon = icon

    def setUrgency(self, urgency):
        """ Set notification's urgency. """
        if method != "pynotify":
            return  # urgency's used only with pynotify method
        if urgency == "low":
            self.urgency = pynotify.URGENCY_LOW
        elif urgency == "normal":
            self.urgency = pynotify.URGENCY_NORMAL
        elif urgency == "critical":
            self.urgency = pynotify.URGENCY_CRITICAL
        else:
            self.urgency = None

    def setTimeout(self, timeout):
        """ Set notification's timeout. """
        self.timeout = timeout

    def show(self):
        if not self.initialized or method is None or self.title is None or self.message is None:
            return
        if method == "pynotify":
            self.notify.update(self.title, self.message, self.icon)
            if self.urgency is not None:
                self.notify.set_urgency(self.urgency)
            self.notify.set_timeout(self.timeout)
            self.notify.show()
        if method == "dbus":
            interface = self.__connect()
            if interface is not None:
                interface.Notify(
                    APP_NAME,
                    0,
                    self.icon,
                    self.title,
                    self.message,
                    "",
                    "",
                    self.timeout)
