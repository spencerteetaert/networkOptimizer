from networkClasses import *

class TowerConnection:
	def __init__(self, tower1, tower2, maxBandWidth, active):
		self.tower1 = tower1
		self.tower2 = tower2
		self.maxBandWidth = maxBandWidth
		self.remainingBandWidth = maxBandWidth
		self.parent = 1
		self.active = active
		self.stdDev = 0.1 * maxBandWidth

	def GetOtherTower(self, ID):
		if (ID == self.tower2.GetID()):
			return self.tower1
		if (ID == self.tower1.GetID()):
			return self.tower2

		return 0

	def GetMaxBandWidth(self):
		return self.maxBandWidth

	def AddToBandWidth(self, toAdd):
		self.remainingBandWidth -= toAdd
		return 0

	def GetRemainingBandWidth(self):
		return self.remainingBandWidth

	def GetHealth(self):
		if (self.remainingBandWidth > self.stdDev):
			return (self.remainingBandWidth - self.stdDev)*0.001
		elif (self.remainingBandWidth <= self.stdDev) & (self.remainingBandWidth > 0):
			return -1
		else:
			return -5
			#return self.remainingBandWidth

	def IsParent(self, incomingID):
		if (incomingID == self.tower1.GetID() & self.parent == 1):
			return True
		if (incomingID == self.tower2.GetID() & self.parent == 2):
			return True

		return False

	def GetStatus(self):
		return self.active

	def Reset(self):
		self.parent = 1
		self.remainingBandWidth = self.maxBandWidth