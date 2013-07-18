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

from time import strftime

class Log():
	def __init__(self, logfile):
		self.logfile = logfile
		self.log = None

	def __open(self):
		""" Open log file for writing. """
		try:
			self.log = open(self.logfile, "a+")
		except:
			self.log = None

	def __close(self):
		""" Close log file. """
		if self.log != None:
			self.log.close()

	def __get_time(self):
		""" Return current time string. """
		return strftime("%a %d %H:%M:%S : ")

	def write(self, message):
		self.__open()
		if self.log == None:
			return
		line = self.__get_time() + message + "\n"
		self.log.write(line)
		self.__close()
