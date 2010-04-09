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
import subprocess
import dbus.service

from backends.globals import *

class Cpu(dbus.service.Object):
	""" Handle CPU informations """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
			
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsTemperatureAvailable(self, sender = None, conn = None):
		""" Return 'True' if temperature reading is available, 'False' otherwise. """
		if os.path.exists(CPU_TEMPERATURE_PATH):
			return True
		else:
			return False
	
	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetTemperature(self, sender = None, conn = None):
		""" Return current CPU temperature. """
		""" Return 'none' if any error. """
		if not self.IsTemperatureAvailable():
			return "none"
		try:
			file = open(CPU_TEMPERATURE_PATH, "r")
		except:
			systemlog.write("ERROR: 'Cpu.GetTemperature()' - Cannot read temperature from '" + CPU_TEMPERATURE_PATH + "'.")
			return "none"
		return file.read().split(':')[1].strip()
