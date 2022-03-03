import time
from collections import deque
import re

#For the board class I tried to use as few loops as possible.
#Especially considering we know that at most each node has 4 children that
#represent each movement direction.

#NOTE: In the childList the index 0 is the left most child and index 3 is the right most child.
#In a tree that only has 2 children to a parent node, index 0 is left most child and index 1 is right most child.
class Board:
	def __init__(self, state):
		self.state = state
		self.childrenList = []
		self.parent = None
		self.depth = 0
		self.expanded = False
		
		#Used with A* implementation.
		self.f = 0
		self.h = 0
		self.g = 0

	#Function to generate the list of child boards.
	def generateChildList(self):
		#--TODO-- make sure children are legal and not the same as parent.
		tempState = self.state
		temp = Board(self.up(tempState))
		temp2 = Board(self.down(tempState))
		temp3 = Board(self.left(tempState))
		temp4 = Board(self.right(tempState))

		#Set child depth.
		temp.depth = self.depth + 1
		temp2.depth = self.depth + 1
		temp3.depth = self.depth + 1
		temp4.depth = self.depth + 1

		#Check to make sure that a child does not have the same board layout as a parent.
		#If the parent is not the solved state, then a child with that same state will not be solved.
		if temp.state != None: 
				self.childrenList.append(temp)
		if temp2.state != None: 
				self.childrenList.append(temp2)
		if temp3.state != None: 
				self.childrenList.append(temp3)
		if temp4.state != None:
				self.childrenList.append(temp4)

	#Board moves. (Up,Down,Left,Right)
	#If the 0 is in the top line, it cant go up.
	def up(self, state):
		position = state.index(0)

		#Check for an illegal move.
		if position in (0,1,2):
			return None
		else:
			#Create a temp list for the new positions.
			newPositions = list(state)
			#Swap the positions of the board.
			newPositions[position], newPositions[position-3] = newPositions[position-3], newPositions[position]
            #Return the new list of positions.
			return tuple(newPositions)

    #If the 0 is in the bottom line, it cant go down.
	def down(self, state):
		position = state.index(0)

 		#Check for an illegal move.
		if position in (6,7,8):
			return None
		else:
			#Create a temp list for the new positions.
			newPositions = list(state)
			#Swap the positions of the board.
			newPositions[position], newPositions[position+3] = newPositions[position+3], newPositions[position]
            #Return the new list of positions.
			return tuple(newPositions)

    #If the 0 is in the left most side, it cant go left. 
	def left(self, state):
		position = state.index(0)

		#Check for an illegal move.
		if position in (0,3,6):
			return None
		else:
			#Create a temp list for the new positions.
			newPositions = list(state)
			#Swap the positions of the board.
			newPositions[position], newPositions[position-1] = newPositions[position-1], newPositions[position]
            #Return the new list of positions.
			return tuple(newPositions)

    #If the 0 is in the rightmost side, it cant go right.
	def right(self, state):
		position = state.index(0)

		#Check for an illegal move.
		if position in (2,5,8):
			return None
		else:
			#Create a temp list for the new positions.
			newPositions = list(state)
			#Swap the positions of the board.
			newPositions[position], newPositions[position+1] = newPositions[position+1], newPositions[position]
            #Return the new list of positions.
			return tuple(newPositions)

###################
#UTILITY FUNCTIONS#
###################

#Set the parents of all child nodes.
def setNodeParents(parent, childList):
		parentNode = parent
		childNodeList = childList

		for child in childNodeList:
			child.parent = parentNode

#Create the path of the states.
def backtraceParents(parentObj):
	pathArray = []

	while parentObj.parent != None:
		pathArray.append(parentObj)
		parentObj = parentObj.parent
	pathArray.reverse()

	return pathArray

#Heuristics
#Misplaced Tiles. This heuristic finds the total number of all tiles that are not in their correct position.
def misplacedTilesHeuristic(stateObj, goal):
	sum = 0

	for elem in range(len(goal)):
	 	if goal[elem] != stateObj.state[elem]:
	 		sum+=1

	return sum

#Manhattan Distance. This heuristic determines how far away each tile is from its goal location.
def manhattanDistanceHeuristic(stateObj, goal):
	temp = stateObj.state
	sum = 0

	for i,item in enumerate(temp):
		previousRow, previousCol = int(i / 3), i % 3 
		goalRow, goalCol = int(item / 3), item % 3
		sum += abs(previousRow - goalRow) + abs(previousCol - goalCol)
	return sum

def A_Star_Misplaced(startState, endState):
	#Set of states that have being visited from the graph.
	closedStates = set()

	frontierStates = set()

	#Set of states that are in the frontier.
	frontier = set()

	currentState = startState

	frontier.add(currentState)

	while frontier:

		#Find the board state in the frontier that has the lowest f value..
		currentState = min(frontier, key=lambda obj:obj.f)
		frontierStates.add(currentState.state)

		#Remove the board from the frontier.
		frontier.remove(currentState)

		#Add the board to the closed set.
		closedStates.add(currentState.state)

		#Compare the currentState's state to the goalState.
		if currentState.state == endState:
			return currentState.state, currentState.depth, currentState

		#Generate the childs children so the search can continue. 
		#This creates a part of the next layer of the tree.
		currentState.generateChildList()

		#This loop peeks at each of the current states neighbors and decides if they have
		#being visited yet. If they have not being visited then they are added to the queue.
		for child in currentState.childrenList:
			#Check to make sure that the child is not already a closed state.
			if child.state not in closedStates:
				frontier.add(child)
				#Check to see if the child is already in the frontier
				if len(frontier) > 0:
					if child.state in frontierStates:
						tempG = currentState.g + 1
						if elem.g > tempG:
							#If g is greater than the value in the frontier, set the current child to that old frontier value.
							elem.g = tempG
							elem.parent = currentState
					else:
						#Generate the f, g, h values.
						child.g = currentState.g + 1
						child.h = misplacedTilesHeuristic(child, endState)
						child.f = child.g + child.h

						#Set the parent of the child to the currentState.
						child.parent = currentState

				else:
					#Generate the f, g, h values.
					child.g = currentState.g + 1
					child.h = misplacedTilesHeuristic(child, endState)
					child.f = child.g + child.h

					#Set the parent ofthe child to the currentState.
					child.parent = currentState

		frontierStates.remove(currentState.state)

	return currentState, currentState.depth, currentState


def A_Star_Manhattan_Distance(startState, endState):
	#Set of states that have being visited from the graph.
	closedStates = set()

	frontierStates = set()

	#Set of states that are in the frontier.
	frontier = set()

	currentState = startState

	frontier.add(currentState)

	while frontier:

		#Find the board state in the frontier that has the lowest f value..
		currentState = min(frontier, key=lambda obj:obj.f)
		frontierStates.add(currentState.state)

		#Remove the board from the frontier.
		frontier.remove(currentState)

		#Add the board to the closed set.
		closedStates.add(currentState.state)

		#Compare the currentState's state to the goalState.
		if currentState.state == endState:
			return currentState.state, currentState.depth, currentState

		#Generate the childs children so the search can continue. 
		#This creates a part of the next layer of the tree.
		currentState.generateChildList()

		#This loop peeks at each of the current states neighbors and decides if they have
		#being visited yet. If they have not being visited then they are added to the queue.
		for child in currentState.childrenList:
			#Check to make sure that the child is not already a closed state.
			if child.state not in closedStates:
				frontier.add(child)
				#Check to see if the child is already in the frontier
				if len(frontier) > 0:
					if child.state in frontierStates:
						tempG = currentState.g + 1
						if elem.g > tempG:
							#If g is greater than the value in the frontier, set the current child to that old frontier value.
							elem.g = tempG
							elem.parent = currentState
					else:
						#Generate the f, g, h values.
						child.g = currentState.g + 1
						child.h = manhattanDistanceHeuristic(child, endState)
						child.f = child.g + child.h

						#Set the parent of the child to the currentState.
						child.parent = currentState

				else:
					#Generate the f, g, h values.
					child.g = currentState.g + 1
					child.h = manhattanDistanceHeuristic(child, endState)
					child.f = child.g + child.h

					#Set the parent ofthe child to the currentState.
					child.parent = currentState

		frontierStates.remove(currentState.state)

	return currentState, currentState.depth, currentState

def print_result(stepsListMisplaced, timeListMisplaced,stepsListManhattan, timeListManhattan, parentObjMisplaced, parentObjManhattan):
	#BFS Backtrace as the sample output.
	pathArrayMisplaced = backtraceParents(parentObjMisplaced)
	pathArrayManhattan = backtraceParents(parentObjManhattan)

    #Print the BFS path.
	counterMisplaced = len(pathArrayMisplaced)

	print("Misplaced Path:")

	print(str(pathArrayMisplaced[0].parent.state[0]) + " " + str(pathArrayMisplaced[0].parent.state[1]) + " " + str(pathArrayMisplaced[0].parent.state[2]))

	print(str(pathArrayMisplaced[0].parent.state[3]) + " " + str(pathArrayMisplaced[0].parent.state[4]) + " " + str(pathArrayMisplaced[0].parent.state[5]))

	print(str(pathArrayMisplaced[0].parent.state[6]) + " " + str(pathArrayMisplaced[0].parent.state[7]) + " " + str(pathArrayMisplaced[0].parent.state[8]) + "\n")

	print("to\n")

	for obj in pathArrayMisplaced:
		counterMisplaced -= 1

		print(str(obj.state[0]) + " " + str(obj.state[1]) + " " + str(obj.state[2]))

		print(str(obj.state[3]) + " " + str(obj.state[4]) + " " + str(obj.state[5]))

		print(str(obj.state[6]) + " " + str(obj.state[7]) + " " + str(obj.state[8]) + "\n")

		if counterMisplaced >= 1:
			print("to\n")

    #Print the DFS path.
	counterManhattan = len(pathArrayManhattan)

	print("Manhattan Path:")

	print(str(pathArrayManhattan[0].parent.state[0]) + " " + str(pathArrayManhattan[0].parent.state[1]) + " " + str(pathArrayManhattan[0].parent.state[2]))

	print(str(pathArrayManhattan[0].parent.state[3]) + " " + str(pathArrayManhattan[0].parent.state[4]) + " " + str(pathArrayManhattan[0].parent.state[5]))

	print(str(pathArrayManhattan[0].parent.state[6]) + " " + str(pathArrayManhattan[0].parent.state[7]) + " " + str(pathArrayManhattan[0].parent.state[8]) + "\n")

	print("to\n")

	for obj in pathArrayManhattan:
		counterManhattan -= 1

		print(str(obj.state[0]) + " " + str(obj.state[1]) + " " + str(obj.state[2]))

		print(str(obj.state[3]) + " " + str(obj.state[4]) + " " + str(obj.state[5]))

		print(str(obj.state[6]) + " " + str(obj.state[7]) + " " + str(obj.state[8]) + "\n")

		if counterManhattan >= 1:
			print("to\n")

	stepSumMisplaced = 0
	timeSumMisplaced = 0

	#Average steps.
	for step in stepsListMisplaced:
			stepSumMisplaced += step
	averageStepsMisplaced = stepSumMisplaced / len(stepsListMisplaced)

	#Average Time.
	for t in timeListMisplaced:
			timeSumMisplaced += t
	averageTimeMisplaced = timeSumMisplaced / len(timeListMisplaced)

	stepSumManhattan = 0
	timeSumManhattan = 0

	#Average steps.
	for step in stepsListManhattan:
			stepSumManhattan += step
	averageStepsManhattan = stepSumManhattan / len(stepsListManhattan)

	#Average Time.
	for t in timeListManhattan:
			timeSumManhattan += t
	averageTimeManhattan = timeSumManhattan / len(timeListManhattan)

	#Print the steps results.
	print("                                Average_Steps                               Average_Time ")
	print("Misplaced                       Depth: " + str(averageStepsMisplaced) + "                          " + str(round(averageTimeMisplaced, 2)) + " Seconds")
	print("Manhattan                       Depth: " + str(averageStepsManhattan) + "                          " + str(round(averageTimeManhattan, 2)) + " Seconds")

###################
#DRIVER CODE HERE.#
###################

# The board looks like this.
#
# |0|1|2|
# |3|4|5|
# |6|7|8|
# 

parentMisplaced = None
parentManhattan = None
stepsListMisplaced = []
timeListMisplaced = []
stepsListManhattan = []
timeListManhattan = []

counter = 0

with open("input.txt", 'r') as infile:
	for line in infile:
		counter += 1

		#print("\nManhattan Test Number: " + str(counter))

		numFilter = filter(str.isdigit, line)
		numString = "".join(numFilter)
		resultList = [int(j) for j in numString]
		resultTuple = tuple(resultList)

		goalTup = (0, 1, 2, 3, 4, 5, 6, 7, 8)

		rootBoard = Board(resultTuple)

		#print("Root state:" + str(rootBoard.state) + "\n")
		setNodeParents(rootBoard, rootBoard.childrenList)
		#Get the current time at the start of the program.
		timeStart = time.time()
		#Run BFS.
		resultManhattan, stepsManhattan, solutionObjectManhattan = A_Star_Manhattan_Distance(rootBoard, goalTup)
		#Get the time at the end of the program.
		timeEnd = time.time()
		#Calculate the difference and add it to the time list.
		totalTime = timeEnd - timeStart

		timeListManhattan.append(totalTime)
		stepsListManhattan.append(stepsManhattan)

		#print("Solution: " + str(resultManhattan))

		#BFS vars.
		parentManhattan = solutionObjectManhattan

counter = 0

with open("input.txt", 'r') as infile:
	for line in infile:
		counter += 1

		#print("\nMisplaced Test Number: " + str(counter))

		numFilter = filter(str.isdigit, line)
		numString = "".join(numFilter)
		resultList = [int(j) for j in numString]
		resultTuple = tuple(resultList)

		goalTup = (0, 1, 2, 3, 4, 5, 6, 7, 8)

		rootBoard = Board(resultTuple)

		#print("Root state:" + str(rootBoard.state) + "\n")
		setNodeParents(rootBoard, rootBoard.childrenList)
		#Get the current time at the start of the program.
		timeStart = time.time()
		#Run BFS.
		resultMisplaced, stepsMisplaced, solutionObjectMisplaced = A_Star_Misplaced(rootBoard, goalTup)
		#Get the time at the end of the program.
		timeEnd = time.time()
		#Calculate the difference and add it to the time list.
		totalTime = timeEnd - timeStart

		timeListMisplaced.append(totalTime)
		stepsListMisplaced.append(stepsMisplaced)

		#print("Solution: " + str(resultMisplaced))

		#BFS vars.
		parentMisplaced = solutionObjectMisplaced

print_result(stepsListMisplaced, timeListMisplaced, stepsListManhattan, timeListManhattan, solutionObjectMisplaced, solutionObjectManhattan)
