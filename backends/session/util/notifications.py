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

from backends.globals import *

try:
	import pynotify
	method = "pynotify"
except:
	sessionlog.write("ERROR: 'notifications'  - cannot import pynotify.")
	method = None
	pass

class Notification():
	""" Show user's notifications. """
	def __init__(self, title = None, message = None, icon = None, urgency = "normal"):
		self.initialized = False # Is notification system initialized
		if method == "pynotify":
			if not pynotify.init("Samsung-Tools Notification System"):
				sessionlog.write("ERROR: 'Notification()'  - cannot initialize pynotify.")
				return
			# Create a new notification
			self.notify = pynotify.Notification(" ")
			# Set initial values
			self.setTitle(title)
			self.setMessage(message)
			self.setIcon(icon)
			self.setUrgency(urgency)
			self.initialized = True

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
			return
		if urgency == "low":
			self.urgency = pynotify.URGENCY_LOW
		elif urgency == "normal":
			self.urgency = pynotify.URGENCY_NORMAL
		elif urgency == "critical":
			self.urgency = pynotify.URGENCY_CRITICAL
		else:
			self.urgency = None
	
	def show(self):
		if not self.initialized or method == None or self.title == None or self.message == None:
			return
		if method == "pynotify":
			self.notify.update(self.title, self.message, self.icon)
			if self.urgency != None:
				self.notify.set_urgency(self.urgency)
			self.notify.show()
