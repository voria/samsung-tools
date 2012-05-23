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
import dbus.service

from backends.globals import *

PHC_VIDS_CPU0 = "/sys/devices/system/cpu/cpu0/cpufreq/phc_vids"
PHC_VIDS_CPU1 = "/sys/devices/system/cpu/cpu1/cpufreq/phc_vids"
PHC_DEFAULT_VIDS = "/sys/devices/system/cpu/cpu0/cpufreq/phc_default_vids"
PHC_FIDS = "/sys/devices/system/cpu/cpu0/cpufreq/phc_fids"
PHC_FREQS = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies"

class Cpu(dbus.service.Object):
	""" Handle CPU informations """
	def __init__(self, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsPHCAvailable(self, sender = None, conn = None):
		if os.path.exists(PHC_VIDS_CPU0):
			return True
		else:
			return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetCurrentVids(self, sender = None, conn = None):
		if not self.IsPHCAvailable():
			return "none"
		try:
			file = open(PHC_VIDS_CPU0, "r")
			vids = file.readline().strip()
			file.close()
			return vids
		except:
			systemlog.write("ERROR: 'Cpu.GetCurrentVids()' - Cannot read from '" + PHC_VIDS_CPU0 + "'.")
			return "none"

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = 's', out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetCurrentVids(self, value, sender = None, conn = None):
		if not self.IsPHCAvailable():
			return False
		try:
			file = open(PHC_VIDS_CPU0, "w")
			file.write(value)
			file.close()
			try: # try to write new values for cpu1 too
				file = open(PHC_VIDS_CPU1, "w")
				file.write(value)
				file.close()
			except:
				pass
			return True
		except:
			systemlog.write("ERROR: 'Cpu.SetCurrentVids()' - Cannot write new values.")
			return False

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetDefaultVids(self, sender = None, conn = None):
		if not self.IsPHCAvailable():
			return "none"
		try:
			file = open(PHC_DEFAULT_VIDS, "r")
			vids = file.readline().strip()
			file.close()
			return vids
		except:
			systemlog.write("ERROR: 'Cpu.GetDefaultVids()' - Cannot read from '" + PHC_DEFAULT_VIDS + "'.")
			return "none"

	@dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature = None, out_signature = 's',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def GetFrequencies(self, sender = None, conn = None):
		try:
			file = open(PHC_FREQS, "r")
			freqs = file.readline().strip().split()
			file.close()
			result = ""
			for freq in freqs:
				result = result + str(int(freq) / 1000) + " "
			return result.strip()
		except:
			systemlog.write("ERROR: 'Cpu.GetFrequencies()' - Cannot read from '" + PHC_FREQS + "'.")
			return "none"

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
		return str(float(file.read()) / 1000)
