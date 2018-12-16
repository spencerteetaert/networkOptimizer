from networkClasses import *

class ClientConnection:
	def __init__(self, clientID, histogram, tower):
		self.histogram = histogram
		self.tower = tower
		self.ID = clientID

	def GetBandWidth(self, halfHour):
		return self.histogram[halfHour]

	def GetID(self):
		return self.ID