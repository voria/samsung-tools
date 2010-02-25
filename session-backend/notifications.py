import pynotify

class Notification():
	def __init__(self, title = None, message = None, icon = None, urgency = "normal"):
		if not pynotify.init("Notification"):
			return None
		# Create a new notification
		self.notify = pynotify.Notification(" ")
		# Set initial values
		self.setTitle(title)
		self.setMessage(message)
		self.setIcon(icon)
		self.setUrgency(urgency)

	def setTitle(self, title):
		self.title = title

	def setMessage(self, message):
		self.message = message

	def setIcon(self, icon):
		self.icon = icon

	def setUrgency(self, urgency):
		if urgency == "low":
			self.urgency = pynotify.URGENCY_LOW
		elif urgency == "normal":
			self.urgency = pynotify.URGENCY_NORMAL
		elif urgency == "critical":
			self.urgency = pynotify.URGENCY_CRITICAL
		else:
			self.urgency = None
	
	def show(self):
		if self.title == None or self.message == None:
			return
		self.notify.update(self.title, self.message, self.icon)
		if self.urgency != None:
			self.notify.set_urgency(self.urgency)
		self.notify.show()

if __name__ == "__main__":
	# Test routine
	n = Notification()
	n.setTitle("Title")
	n.setMessage("Message")
	n.setIcon("info")
	n.setUrgency("critical")
	n.show()
