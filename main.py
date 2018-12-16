import random
import copy
from networkClasses import *
###Underlaying algorithm idea:
###First: Iterate through the network from out to in, finding paths of least resistence and updating accordingly
###Second: Compare the overall health of the generated network using this specific order relative to the best found health
###Third: Replace order with new order if it was better
###Fourth: Change some tower orders by natural selection and repeat

###Run throuhg X iterations documenting results, find a more optimized network 
### --- No guarantee this will produce the absolute best network but will greatly improve


def main():
	towerData = ImportData('networkData.csv')

	#print("Pre evolution data:\n")
	#for i in range(0, len(towerData), 1):
	#	towerData[i].PrintData()

	oldOldNetworkStrength = 0
	winningNetworkData = list(towerData)

	for i in range(0,5000,1):
		towerData = BuildOptimalNetwork(towerData)
		oldNetworkStrength = GetNetworkCondition(towerData)

		temp = list(towerData)
		towerData = ResetTowerData(towerData)

		towerData = Evolve(towerData)
		towerData = BuildOptimalNetwork(towerData)
		newNetworkStrength = GetNetworkCondition(towerData)

		if (oldNetworkStrength > newNetworkStrength):
			towerData = list(temp)
		else:
			winningNetworkData = copy.deepcopy(towerData)
			#print("test",winningNetworkData[1].GetTowerConnections()[0].GetRemainingBandWidth())
			if (newNetworkStrength != oldNetworkStrength):
				print("New win:",newNetworkStrength)

		towerData = ResetTowerData(towerData)

	print("\nPost evolution data:\n\n   Evolved network strength:",GetNetworkCondition(winningNetworkData),"\n")

	for i in range(0, len(towerData), 1):
		winningNetworkData[i].PrintData()

	wait = input("Press ENTER to continue")
	return 0

###Identifies towers that are not connected to the network
###Finds path of least resistance from each tower to the data center 
def BuildOptimalNetwork(networkData):
	###Attempt 1: Modified Dijkstra's Algorithm 
	###First, set all costs to infinity except the start node
	###Then, Run through each adjacent node, updating only if the new cost if lower
	###Update costs and run back to "Finish Node"

	###After adding a new path update the remaining bandwidths of each connection in said path
	###This will allow for in the future, changing the health of the network by adjusting the order which we make paths
	###We will make new paths through the process of evolution, until an optimal one is reached 

	connectedTowers = []

	for k in range(0, len(networkData),1):
		if networkData[k].GetID() == 1:
			continue
	#for k in range(9, 10, 1):
		#print("\n \n Now looking at tower ###",k+1)
		visitedTowerIDs = []
		paths = [[networkData[k]]]

		for i in range(0, len(networkData),1):
			networkData[i].SetCost(float("inf"))

		###Algorithm for one tower 
		currentTower = networkData[k]
		currentTower.SetCost(0)
		targetTower = FindTargetTower(networkData)
		visitedTowerIDs += [currentTower.GetID()]

		while True: #Breaks when the Data Center node is found
			#print("\n \n ###New connection")
			#print("Current tower is:",currentTower.GetID())
			###Runs through each tower connection of current node
			for j in range(0, len(currentTower.GetTowerConnections()), 1):
				###First check if we have already visited the node
				otherTower = currentTower.GetTowerConnections()[j].GetOtherTower(currentTower.GetID())

				if (otherTower.GetID() not in visitedTowerIDs):
					###If weight of tower on other end of connection is more than this path's weight -> change other tower's weight
					if (currentTower.GetTowerConnections()[j].GetRemainingBandWidth() != 0):
						if (otherTower.GetCost() > currentTower.GetCost() + 1 / currentTower.GetTowerConnections()[j].GetRemainingBandWidth()):
							#print("Tower:",otherTower.GetID(),"cost was updated to:",currentTower.GetCost() + 1 / currentTower.GetTowerConnections()[j].GetRemainingBandWidth())
							#print("Current tower bandwidth:",currentTower.GetTowerConnections()[j].GetRemainingBandWidth(),"Tower:",currentTower.GetID())
							otherTower.SetCost(currentTower.GetCost() + 1 / currentTower.GetTowerConnections()[j].GetRemainingBandWidth())
							otherTower.SetFrom(currentTower.GetID())
					else:
						otherTower.SetCost(currentTower.GetCost() + 10000)
						otherTower.SetFrom(currentTower.GetID())

				#	else:
				#		print("Tower:",otherTower.GetID(),"was checked but weight was not updated")
				#else:
				#	print("Other tower:",otherTower.GetID()," was found in visitedTowerIDs:",visitedTowerIDs)

			###Finds new lowest 
			currentLowestCost = float("inf")

			for i in range(0,len(networkData),1):
				if (networkData[i].GetID() not in visitedTowerIDs) & (networkData[i].GetCost() < currentLowestCost):
					currentLowestCost = networkData[i].GetCost()
					currentLowestTower = networkData[i]

			if (currentLowestCost == float("inf")):
				#print("ERR: Tower",networkData[k].GetID(),"is disconnected from the network")
				networkData[k].SetIsConnected(False)
				break


			###Finds the path from starting tower to data center
			flag = False
			for i in range(0,len(paths),1):
				if (currentLowestTower.GetFrom() == paths[i][len(paths[i])-1].GetID()):
					paths[i] = paths[i] + [currentLowestTower]
					flag = True
					#print("Added to path:",end=" ")
					#for o in range(0, len(paths[i]),1):
					#	print(paths[i][o].GetID(),end=" ")

			if (flag == False):
				for c1 in range(0,len(paths),1):
					for c2 in range(0,len(paths[c1]),1):
						if (paths[c1][c2].GetID() == currentLowestTower.GetFrom()):
							paths += [paths[c1][:c2+1]]
							paths[len(paths)-1] += [currentLowestTower]
							flag = True
							break
					if (flag == True):
						break


			currentTower = currentLowestTower
			visitedTowerIDs += [currentTower.GetID()]
			#print("Current tower was set to:",currentTower.GetID(),"from:",currentLowestTower.GetFrom())

			###Triggers once destination node is found
			if (currentTower == targetTower):
				###Finds shortest path
				for i in range(0,len(paths),1):
					#print("(",k+1,") Last tower in each path:",paths[i][len(paths[i])-1].GetID())
					if paths[i][len(paths[i])-1] == targetTower: ##This is never true for 10.. why?
						#print("Path[i][0]:",paths[i][0].GetID())
						shortestPath = paths[i]
						break

				###Adds shortest path to connected towers (to be used to check weights later)
				connectedTowers += shortestPath
				connectedTowers = RemoveDuplicates(connectedTowers)

				networkData = UpdateBandWidth(shortestPath, networkData)
				networkData = ClearFroms(networkData)

				toPrint = []
				for i in range(0,len(shortestPath),1):
					toPrint += [shortestPath[i].GetID()]
				networkData[k].SetPath(toPrint)
				#print("Success: Tower",toPrint[0],"optimal path is:",toPrint)
				break

	#print(connectedTowers) ##FIX: Make so there are no repeats
	return networkData

def FindTargetTower(networkData):
	for i in range(0, len(networkData),1):
		if networkData[i].IsDataCenter() == True:
			return networkData[i]
	return 0

###Returns the overall health of a given network using connection load as fitness
def GetNetworkCondition(networkData):
	connectionHealth = 0
	for i in range(0, len(networkData),1):
		for j in range(0, len(networkData[i].GetTowerConnections()),1):
			if networkData[i].GetTowerConnections()[j].GetOtherTower(networkData[i].GetID()).GetID() > networkData[i].GetID():
				connectionHealth += networkData[i].GetTowerConnections()[j].GetHealth()

	#print("Network strength:",connectionHealth/connectionCount*100,"%")
	return connectionHealth

def UpdateBandWidth(shortestPath, networkData):
	for i in range(0,len(shortestPath),1):
		for j in range(0,len(shortestPath[i].GetTowerConnections()),1):
			#print("Other tower ID:",shortestPath[i].GetTowerConnections()[j].GetOtherTower(shortestPath[i].GetID()).GetID())
			#print("From:",shortestPath[i].GetFrom())
			otherTower = shortestPath[i].GetTowerConnections()[j].GetOtherTower(shortestPath[i].GetID())
			if (otherTower.GetID() == shortestPath[i].GetFrom()) & (otherTower in shortestPath):
				shortestPath[i].GetTowerConnections()[j].AddToBandWidth(shortestPath[0].GetLoad())
				#print("back- Bandwidth between towers",otherTower.GetID(),"and",shortestPath[i].GetID(),"reduced to",shortestPath[i].GetTowerConnections()[j].GetRemainingBandWidth())
				for j in range(0, len(networkData),1):
					if (networkData[j].GetID() == shortestPath[i].GetID()):
						networkData[j] = shortestPath[i]				
						break
			elif (otherTower.GetFrom() == shortestPath[i].GetID()) & (otherTower in shortestPath):
				shortestPath[i].GetTowerConnections()[j].AddToBandWidth(shortestPath[0].GetLoad()) 
				#print("Bandwidth between towers",otherTower.GetID(),"and",shortestPath[i].GetID(),"reduced to",shortestPath[i].GetTowerConnections()[j].GetRemainingBandWidth())
				for j in range(0, len(networkData),1):
					if (networkData[j].GetID() == shortestPath[i].GetID()):
						networkData[j] = shortestPath[i]				
						break

	return networkData

def Evolve(networkData):
	for i in range(0,len(networkData),1):
		if (random.randint(0,10) < 4) & (i < (len(networkData)-1)):
			temp = networkData[i]
			networkData[i] = networkData[i+1]
			networkData[i+1] = temp
		if (random.randint(0,10) < 3) & (i != 0):
			temp = networkData[i]
			networkData[i] = networkData[i-1]
			networkData[i-1] = temp

	return networkData

def ResetTowerData(networkData):
	for i in range(0, len(networkData),1):
		networkData[i].Clear()
	return networkData

###Imports data from 'networkData.csv'
###Creates a datastructure with ret[] = Tower
def ImportData(fileName):
	file = open(fileName, 'r')
	ret = []

	while True:
		line = file.readline().split(",")
		currentTowerID = 0
		client = False
		clientCount = 0

		###Breaks at the end of the CSV document
		if (line == ['']):
			break

		counter = 0
		while (line[counter] != 'x') & (line[counter] != 'x\n'):
			if(line[counter] == 'Tower'):
			    currentTowerID = int(line[counter+1])
			    towerLoad = float(line[counter+3])
			    ret += [Tower(currentTowerID,towerLoad)]
			    counter += 3
			if (line[counter] == 'DataCenterConnection'):
				ret[currentTowerID-1].MakeDataCenterConnection(int(line[counter+1]))
				counter += 1
			if(line[counter] == 'TowerConnection'): 
				if (currentTowerID > int(line[counter + 1])): ###Only adds a connection if the linked towewr already exists
					ret[currentTowerID-1].MakeTowerConnection(ret[int(line[counter + 1]) - 1], int(line[counter + 2]), True)
				counter+=2
			if(line[counter] == 'Client'):
				histogram = []
				for i in range(2, 50, 1):
					histogram += [float(line[counter + i])]
				ret[currentTowerID-1].MakeClientConnection(int(line[counter + 1]), histogram)
				clientCount = 0
				counter += 48

			counter+=1
	
	file.close()
	return ret

def RemoveDuplicates(lis):
	ret = []
	for i in range(0,len(lis),1):
		if (lis[i] not in ret):
			ret += [lis[i]]

	return ret

def ClearFroms(networkData):
	for i in range(0, len(networkData),1):
		networkData[i].ClearFrom()

	return networkData

main()