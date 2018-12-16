from networkClasses import *

class Tower:
	def __init__(self, ID,Load):
		self.ID = ID
		self.t_connections = []
		self.c_connections = []
		self.dataCenter = False
		self.dataCenterBandWidth = 0
		self.cost = 0
		self.f = 0
		self.load = Load
		self.isConnected = True
		self.optialPath = []

	def MakeTowerConnection(self, otherTower, maxBandWidth, firstInstance):
 		self.t_connections += [TowerConnection(self, otherTower, maxBandWidth, False)]
 		if (firstInstance == True):
 			otherTower.MakeTowerConnection(self, maxBandWidth, False)

	def GetTowerConnections(self):
		return self.t_connections

	def MakeClientConnection(self, clientID, histogram):
 		self.c_connections += [ClientConnection(clientID, histogram, self)]

	def MakeDataCenterConnection(self, maxBandWidth):
 		self.dataCenter = True
 		self.dataCenterBandWidth = maxBandWidth

	def IsDataCenter(self):
 		return self.dataCenter

	def GetTotalDemand(self):
		ret = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		#Runs through each bandwidth section on a client
		for i in range(0,48,1):
			#For each client and tower connection a tower has
			for j in range(0,len(self.c_connections),1):
				ret[i] += self.c_connections[j].GetBandWidth(i)
			for j in range(0,len(self.t_connections),1): #Current problem: when initializing tower connections it's creating a looping network, need to ensure all paths lead to rome.
				if (self.t_connections[j].IsParent(self.ID) == False & self.t_connections[j].GetStatus() == True):
					ret = self.AddHistogram(ret, self.t_connections[j].GetOtherTower(self.ID).GetTotalDemand())

		return ret

	def SetPath(self, path):
		self.optialPath = path

	def GetPath(self):
		return self.optialPath

	def SetIsConnected(self, b):
		self.isConnected = b

	def SetFrom(self, otherTowerID):
		self.f = otherTowerID

	def GetFrom(self):
		return self.f

	def ClearFrom(self):
		self.f = 0

	def AddHistogram(self, ret, histogram):
		for i in range(0,48,1):
			ret[i] += histogram[i]
		return ret

	def GetID(self):
		return self.ID

	def GetLoad(self):
		return self.load

	def SetCost(self, value):
		self.cost = value

	def GetCost(self):
		return self.cost

	def Clear(self):
		self.cost = 0
		self.f = 0
		for i in range(0,len(self.t_connections),1):
			self.t_connections[i].Reset()

	def PrintData(self):
		print("\nTower ID: ", self.ID," Load:",self.load)
		if (self.isConnected == False):
			print("   #ERR: Tower is disconnected from the network")
		print("   Path:", end=" ")
		for i in range(0,len(self.optialPath),1):
			print(self.optialPath[i],end=" ")
		print()
		if (self.dataCenter == True):
			print("   Data center connection max bandwidth:", self.dataCenterBandWidth)
		for i in range(0, len(self.t_connections),1):
			print("   Tower connection:", self.t_connections[i].GetOtherTower(self.ID).GetID(), " Max bandwidth:", self.t_connections[i].GetMaxBandWidth(), " Remaining bandwidth:", self.t_connections[i].GetRemainingBandWidth()," Buffer:",self.t_connections[i].GetMaxBandWidth()*0.1)
			if (self.t_connections[i].GetRemainingBandWidth() < self.t_connections[i].GetMaxBandWidth()*0.1):
				print("   #ERR: Little oof")
			if (self.t_connections[i].GetRemainingBandWidth() < 0):
				print("   #ERR: Big Ooof")
			if (self.t_connections[i].GetRemainingBandWidth() == self.t_connections[i].GetMaxBandWidth()):
				print("   #Connection inactive")

		for i in range(0, len(self.c_connections), 1):
			print("      Client connection:", self.c_connections[i].GetID())
			print("      Histogram data (half hour blocks):", end=" ")
			for j in range(0, 48, 1):
				print(self.c_connections[i].GetBandWidth(j), end=" ")
			print()