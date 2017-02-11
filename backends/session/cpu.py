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

import dbus.service

from backends.globals import *
from backends.session.util.locales import *
from backends.session.util.icons import *


class Cpu(dbus.service.Object):
	""" Control CPU and Fan """
	def __init__(self, notify = None, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.notify = notify

	def __connect_cpu(self):
		""" Enable connection to system backend for 'Cpu' object """
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_CPU)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		sessionlog.write("ERROR: 'Cpu.__connect_cpu()' - 3 attempts to connect to system bus failed.")
		return None

	def __connect_fan(self):
		""" Enable connection to system backend for 'Fan' object """
		retry = 3
		while retry > 0:
			try:
				bus = dbus.SystemBus()
				proxy = bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_FAN)
				return dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
			except:
				retry = retry - 1
		sessionlog.write("ERROR: 'Cpu.__connect_fan()' - 3 attempts to connect to system bus failed.")
		return None

	def __show_notify(self, title, message, icon, urgency = "critical"):
		""" Show user notifications. """
		if self.notify is not None:
			temp = self.GetTemperature()
			if temp != "none":
				message = CPU_TEMPERATURE + " " + temp + unicode(" °C", "utf8") + "\n" + message
			self.notify.setTitle(title)
			self.notify.setMessage(message)
			self.notify.setIcon(icon)
			self.notify.setUrgency(urgency)
			self.notify.show()

	def __fan_not_available(self, show_notify = True):
		""" If show_notify == True, inform the user that the fan control is not available. """
		if show_notify:
			self.__show_notify(CPU_TITLE, FAN_NOT_AVAILABLE, STOP_ICON)

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsFanAvailable(self, sender = None, conn = None):
		""" Check if the fan control is available. """
		""" Return 'True' if available, 'False' if disabled or any error. """
		interface = self.__connect_fan()
		if not interface:
			return False
		return interface.IsAvailable()

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsTemperatureAvailable(self, sender = None, conn = None):
		""" Check if temperature reading is available. """
		""" Return 'True' if available, 'False' if disabled or any error. """
		interface = self.__connect_cpu()
		if not interface:
			return False
		return interface.IsTemperatureAvailable()

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetTemperature(self, sender = None, conn = None):
		""" Get the current CPU temperature. """
		""" Return 'none' if temperature reading is not available. """
		interface = self.__connect_cpu()
		return interface.GetTemperature()

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Status(self, show_notify = True, sender = None, conn = None):
		""" Show current fan mode. """
		"""Return 0 if 'normal', 1 if 'silent', 2 if 'overclock'. """
		""" Return 3 if any error. """
		if not self.IsFanAvailable():
			self.__fan_not_available(show_notify)
			return 3
		interface = self.__connect_fan()
		if not interface:
			return 3
		status = interface.Status()
		if show_notify:
			title = CPU_TITLE
			if status == 0:
				message = FAN_STATUS_NORMAL
				icon = FAN_NORMAL_ICON
			elif status == 1:
				message = FAN_STATUS_SILENT
				icon = FAN_SILENT_ICON
			elif status == 2:
				message = FAN_STATUS_OVERCLOCK
				icon = FAN_OVERCLOCK_ICON
			else:  # status == 3
				self.__fan_not_available(show_notify)
				return 3
			self.__show_notify(title, message, icon)
		return status

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanNormal(self, show_notify = True, sender = None, conn = None):
		""" Set fan to 'normal' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsFanAvailable():
			return self.__fan_not_available(show_notify)
		interface = self.__connect_fan()
		if not interface:
			return False
		result = interface.SetNormal()
		if show_notify:
			if result:
				self.__show_notify(CPU_TITLE, FAN_STATUS_NORMAL, FAN_NORMAL_ICON)
			else:
				self.__show_notify(CPU_TITLE, FAN_SWITCHING_ERROR, ERROR_ICON)
		return result

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanSilent(self, show_notify = True, sender = None, conn = None):
		""" Set fan to 'silent' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsFanAvailable():
			return self.__fan_not_available(show_notify)
		interface = self.__connect_fan()
		if not interface:
			return False
		result = interface.SetSilent()
		if show_notify:
			if result:
				self.__show_notify(CPU_TITLE, FAN_STATUS_SILENT, FAN_SILENT_ICON)
			else:
				self.__show_notify(CPU_TITLE, FAN_SWITCHING_ERROR, ERROR_ICON)
		return result

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetFanOverclock(self, show_notify = True, sender = None, conn = None):
		""" Set fan to 'overclock' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsFanAvailable():
			return self.__fan_not_available(show_notify)
		interface = self.__connect_fan()
		if not interface:
			return False
		result = interface.SetOverclock()
		if show_notify:
			if result:
				self.__show_notify(CPU_TITLE, FAN_STATUS_OVERCLOCK, FAN_OVERCLOCK_ICON)
			else:
				self.__show_notify(CPU_TITLE, FAN_SWITCHING_ERROR, ERROR_ICON)
		return result

	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = 'b', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Cycle(self, show_notify = True, sender = None, conn = None):
		""" Set the next fan mode in a cyclic way. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsFanAvailable():
			return self.__fan_not_available(show_notify)
		interface = self.__connect_fan()
		if not interface:
			return False
		result = interface.Cycle()
		if show_notify:
			title = CPU_TITLE
			if result:
				status = interface.Status()
				if status == 0:
					message = FAN_STATUS_NORMAL
					icon = FAN_NORMAL_ICON
				elif status == 1:
					message = FAN_STATUS_SILENT
					icon = FAN_SILENT_ICON
				elif status == 2:
					message = FAN_STATUS_OVERCLOCK
					icon = FAN_OVERCLOCK_ICON
				else:  # status == 3
					self.__fan_not_available(show_notify)
					return False
			else:  # result == False
				message = FAN_SWITCHING_ERROR
				icon = ERROR_ICON
			self.__show_notify(title, message, icon)
		return result
