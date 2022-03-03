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

#Generates the child layers. Formulates the stack before calling DFS on it.
#My program works for trivial problems with only a few steps.
def Iterative_deepening_dfs(startState, endState):
	#Var to keep track of the current depth.
	depth = 0

	#Used as the stack data structure.
	frontier = deque([startState])

	visitedStates = set(startState.state)

	index = 0

	while frontier:
		#Pop the current state from the head of the queue.
		currentState = frontier.popleft()

		#Compare the currentState's state to the goalState.
		if currentState.state not in visitedStates:
			visitedStates.add(currentState.state)

			if currentState.state == endState:
				#print("Depth: " + str(currentState.depth))
				return currentState, currentState.depth

		#Generate the childs children so the search can continue. 
		#This creates a part of the next layer of the tree.
		#Only create the children if the depth of the child is equal to the current depth.
		#We only need to do this once per layer but we need to check because we visit each node many times over.
		#if currentState.depth == depth:
			currentState.generateChildList()

			#Add the children to the visitedStates set to remake the frontier for the next DFS search.
			#Children must be added after the currentStates position to keep the order.
			counter = 1

			for child in currentState.childrenList:
				#Set the childs parent to the current state.
				child.parent = currentState

				#Add the child to the correct index in the visitedStates list.
				# NOTE: THIS IS PROB WHAT IS SLOWING DOWN THE CODE.
				# LIST INSERTION REQUIRES THAT ALL ELEMENTS SHIFT TO THE RIGHT BY ONE
				frontier.append(child)
				counter += 1

			counter = 0

		if len(frontier) == 0:
		# 	#Increase the depth before the next iteration.
			depth += 1

	return currentState, currentState.depth

#Implement BFS in a layer by layer fashion. Generate one layer of the tree at a time and use BFS to search that layer, 
#then move onto the next layer until a solution is found and return it.
def breadthFirstSearch(startState, endState):
	#Set of states that have being visited from the graph.
	#After a lot of troubleshooting I had to change my entire design and go with
	#a set of tuples rather than a list of lists due to how slow python handles lists.
	#Sets are O(1) on average for searching.
	visitedStates = set()
	#Deque of states to be visted. This is our frontier. 
	#Using collections.deque because pop() for lists is incredibly slow as the list size increases.
	#collections.deque remains average O(1)
	frontier = deque([startState])

	while frontier:
		#Pop the current state from the head of the queue.
		currentState = frontier.popleft()

		#Add the current child to the visited states set.
		visitedStates.add(currentState.state)

		#Compare the currentState's state to the goalState.
		if currentState.state == endState:
			return currentState.state, currentState.depth, currentState

		#Generate the childs children so the search can continue. 
		#This creates a part of the next layer of the tree.
		currentState.generateChildList()

		#This loop peeks at each of the current states neighbors and decides if they have
		#being visited yet. If they have not being visited then they are added to the queue.
		for child in currentState.childrenList:
			if child.state not in visitedStates:
				frontier.append(child)

		#Set the parents of the child states.
		for child in currentState.childrenList:
			child.parent = currentState
    
    #Print the depth.
	return currentState.state, currentState.depth, currentState

def print_result(stepsListBFS, timeListBFS,stepsListIDS, timeListIDS, parentObjBFS, parentObjDFS):
	#BFS Backtrace as the sample output.
	pathArrayBFS = backtraceParents(parentObjBFS)
	pathArrayDFS = backtraceParents(parentObjDFS)

    #Print the BFS path.
	counterBFS = len(pathArrayBFS)

	print("BFS Path:")

	print(str(pathArrayBFS[0].parent.state[0]) + " " + str(pathArrayBFS[0].parent.state[1]) + " " + str(pathArrayBFS[0].parent.state[2]))

	print(str(pathArrayBFS[0].parent.state[3]) + " " + str(pathArrayBFS[0].parent.state[4]) + " " + str(pathArrayBFS[0].parent.state[5]))

	print(str(pathArrayBFS[0].parent.state[6]) + " " + str(pathArrayBFS[0].parent.state[7]) + " " + str(pathArrayBFS[0].parent.state[8]) + "\n")

	for obj in pathArrayBFS:
		counterBFS -= 1

		print(str(obj.state[0]) + " " + str(obj.state[1]) + " " + str(obj.state[2]))

		print(str(obj.state[3]) + " " + str(obj.state[4]) + " " + str(obj.state[5]))

		print(str(obj.state[6]) + " " + str(obj.state[7]) + " " + str(obj.state[8]) + "\n")

		if counterBFS >= 1:
			print("to\n")

    #Print the DFS path.
	counterDFS = len(pathArrayDFS)

	print("DFS Path:")

	print(str(pathArrayDFS[0].parent.state[0]) + " " + str(pathArrayDFS[0].parent.state[1]) + " " + str(pathArrayDFS[0].parent.state[2]))

	print(str(pathArrayDFS[0].parent.state[3]) + " " + str(pathArrayDFS[0].parent.state[4]) + " " + str(pathArrayDFS[0].parent.state[5]))

	print(str(pathArrayDFS[0].parent.state[6]) + " " + str(pathArrayDFS[0].parent.state[7]) + " " + str(pathArrayDFS[0].parent.state[8]) + "\n")

	for obj in pathArrayDFS:
		counterDFS -= 1

		print(str(obj.state[0]) + " " + str(obj.state[1]) + " " + str(obj.state[2]))

		print(str(obj.state[3]) + " " + str(obj.state[4]) + " " + str(obj.state[5]))

		print(str(obj.state[6]) + " " + str(obj.state[7]) + " " + str(obj.state[8]) + "\n")

		if counterDFS >= 1:
			print("to\n")

	stepSumBFS = 0
	timeSumBFS = 0

	#Average steps.
	for step in stepsListBFS:
			stepSumBFS += step
	averageStepsBFS = stepSumBFS / len(stepsListBFS)

	#Average Time.
	for t in timeListBFS:
			timeSumBFS += t
	averageTimeBFS = timeSumBFS / len(timeListBFS)

	stepSumIDS = 0
	timeSumIDS = 0

	#Average steps.
	for step in stepsListIDS:
			stepSumIDS += step
	averageStepsIDS = stepSumIDS / len(stepsListIDS)

	#Average Time.
	for t in timeListIDS:
			timeSumIDS += t
	averageTimeIDS = timeSumIDS / len(timeListIDS)

	#Print the steps results.
	print("                          Average_Steps         Average_Time ")
	print("IDS                       Depth: " + str(averageStepsIDS) + "                          " + str(round(averageTimeIDS, 2)) + " Seconds")
	print("BFS                       Depth: " + str(averageStepsBFS) + "                          " + str(round(averageTimeBFS, 2)) + " Seconds")

###################
#DRIVER CODE HERE.#
###################

# The board looks like this.
#
# |0|1|2|
# |3|4|5|
# |6|7|8|
# 

parentBFS = None
parentDFS = None
stepsListBFS = []
timeListBFS = []
stepsListDFS = []
timeListDFS = []

counter = 0

with open("input.txt", 'r') as infile:
	for line in infile:
		counter += 1

		print("\nIDDFS Test Number: " + str(counter))

		numFilter = filter(str.isdigit, line)
		numString = "".join(numFilter)
		resultList = [int(j) for j in numString]
		resultTuple = tuple(resultList)

		goalTup = (0, 1, 2, 3, 4, 5, 6, 7, 8)

		rootBoard = Board(resultTuple)

		print("Root state:" + str(rootBoard.state))
		setNodeParents(rootBoard, rootBoard.childrenList)

		#Timer.
		timeStartDFS = time.time()
		#Run IDDFS.
		resultDFS, stepsDFS = Iterative_deepening_dfs(rootBoard, goalTup)
		#End timer.
		timeEndDFS = time.time()
		#Total time.
		totalTimeDFS = timeEndDFS - timeStartDFS

		timeListDFS.append(totalTimeDFS)
		stepsListDFS.append(stepsDFS)

		print("Solution: " + str(goalTup))

		#DFS vars.
		parentDFS = resultDFS

counter = 0

with open("input.txt", 'r') as infile:
	for line in infile:
		counter += 1

		print("\nBFS Test Number: " + str(counter))

		numFilter = filter(str.isdigit, line)
		numString = "".join(numFilter)
		resultList = [int(j) for j in numString]
		resultTuple = tuple(resultList)

		goalTup = (0, 1, 2, 3, 4, 5, 6, 7, 8)

		rootBoard = Board(resultTuple)

		print("Root state:" + str(rootBoard.state) + "\n")
		setNodeParents(rootBoard, rootBoard.childrenList)
		#Get the current time at the start of the program.
		timeStart = time.time()
		#Run BFS.
		resultBFS, stepsBFS, solutionObjectBFS = breadthFirstSearch(rootBoard, goalTup)
		#Get the time at the end of the program.
		timeEnd = time.time()
		#Calculate the difference and add it to the time list.
		totalTime = timeEnd - timeStart

		timeListBFS.append(totalTime)
		stepsListBFS.append(stepsBFS)

		print("Solution: " + str(goalTup))

		#BFS vars.
		parentBFS = solutionObjectBFS

print_result(stepsListBFS, timeListBFS, stepsListDFS, timeListDFS, solutionObjectBFS, resultDFS)
