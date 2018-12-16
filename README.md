# NetworkOptimizer


This network optimizer is design to tackle the challenge of finding the best way to connect a wireless network.
It models a network of towers connected to each other with connections of varying capacity. The idea is to find the series of 
paths that each tower can take back to the origin (tower 1) that optimizes the health of the network. 

### Network Health 
The network health is a number that is meant to represent the quality and overall effectiveness of any given network. The goal
is to try to keep the load on any given connection as low as possible, and have at least a 10% buffer to handle unexpected spikes
in data usage. The network health is the fitness variable that determines whether a given evolution of the network survives or not. 

### Algorithm
The algorithm I uses graph theory to find the shortest possible path between nodes. The difficulty with this program is measuring the weight
of a given connection. Because connections that are near fully loaded should not ever be choosen I needed to weight the connections 
base on their remaining bandwidth. Unfortunately it is impossible to know the remiaining bandwidth without first knowing the path. This puts
us in a catch 22. Like my civil engineering professor always says: "To find the answer you must know the answer". 

So how did I tackle this?

I started at tower one, then used Dijkstra's algorithm to find the shortest possible path using the reciprocal remaining bandwidths 
of each connection as my weight. After I found the path back for this tower, I updated the remaining bandwidth values of each connection
that the algorithm chose to go through. I then went to tower number 2 and did the same thing. I repeated this for all towers.

At this point the program has done its best but I still found that it wasn't creating good paths, I could find ways of making it work
by hand that the program couldn't find, it still constantly overloaded specific connections.

### Evolution
This is where the optimization comes in. Through a simple evolution algorithm I began randomly re-ordering the order in which the towers
were fed through the path finding algorithm. This means instead of starting at tower 1 it might start at tower 2 or 3, or any number of tower.
After reordering the list it runs through the pathfinding algorithm again then compares the health of this new network with the health 
of the old network, it then saves the better one. In a reasonable amount of time this evolution of the network seems to find good 
setups such that the network does not have any connections overloaded.

### Next Steps
Currently I am working with my linear algebra professor to modify Google's PageRank algorithm to remove the need for evolution. Evolution
does work but does not guarantee the best outcome, as well, as bigger networks are run through the evolution version sucks up a lot
of processing power. My hope is that if properly manipulated, the PageRank algorithm will hold the key to solving the optimal solution
to this problem. It should also greatly reduce the load on the CPU running the program. 
