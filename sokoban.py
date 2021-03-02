import sys
import collections
import heapq
import time

def generateGameMap(argv): #read the input line by line
    with open('sokobanLevels/' + argv, "r") as f:
        line = f.readline()
        count = 1
        wallPos = []
        boxPos = []
        goalPos = []
        while line:
            line = f.readline()
            count += 1
            s = line.split()
            i = 1
            for i in range(1, len(s), 2): #assign values to different properties
                if count == 2:
                    wallPos.append((int(s[i]), int(s[i+1])))
                elif count == 3:
                    boxPos.append((int(s[i]), int(s[i+1])))   
                elif count == 4:
                    goalPos.append((int(s[i]), int(s[i+1])))  
                elif count == 5:
                    j = 0 
                    playerPos = tuple((int(s[j]), int(s[j+1])))
    return tuple(wallPos), tuple(boxPos), tuple(goalPos), playerPos


def nextMove(playerPos, boxPos):
    """Return all legal moves for the agent in the current game state"""
    x, y = playerPos
    directions = [[-1,0,'U'],[1,0,'D'],[0,-1,'L'],[0,1,'R']] # 4 directions
    correctMoves = []
    for move in directions:  
        newX, newY = x + move[0], y + move[1]
        if (newX, newY) in boxPos: #We should consider the if newBoxPos is reachable when the player pushes a box
            newX += move[0] 
            newY += move[1]
        if (newX, newY) not in boxPos + wallPos: #if newBoxPos doesn't cover other boxes' or wall's position, then this move is correct
            correctMoves.append(move)
        else: 
            continue     
    return tuple(tuple(x) for x in correctMoves) 

def updateState(playerPos, boxPos, move):
    """Return updated game state after an move is taken"""
    x, y = playerPos 
    newX, newY = x + move[0], y + move[1]# the current position of player
    boxPos = [list(x) for x in boxPos]
    if [newX, newY] in boxPos: # if pushing, update the position of box
        boxPos.remove([newX, newY])
        boxPos.append([newX + move[0], newY + move[1]])
    boxPos = tuple(tuple(x) for x in boxPos) #To make it hashable, change it back to tuple 
    newPlayerPos = (newX, newY)
    return newPlayerPos, boxPos

def heuristic(playerPos, boxPos):
    distance = 0
    sortedBoxPos = sorted(list(boxPos))
    sortedGoalPos = sorted(list(goalPos))
    for i in range(len(sortedBoxPos)):
        distance += (abs(sortedBoxPos[i][0] - sortedGoalPos[i][0])) + (abs(sortedBoxPos[i][1] - sortedGoalPos[i][1])) #calculate the total distance of closest box and goal
    return distance

def aStarSearch():
    frontier = []
    moves = []
    step = 0 #tie breaker: when priority are the same
    exploredSet = set()
    priority = heuristic(playerPos, boxPos) #heuristic as priority
    heapq.heappush(frontier, (priority, step, [(playerPos, boxPos)])) #heapq: maintain the priority queue
    heapq.heappush(moves, (priority, step, [0]))

    while frontier:
        state = heapq.heappop(frontier)[-1] #state: [(playerPos, boxPos)]
        strategy = heapq.heappop(moves)[-1] #current:0 moves
        if sorted(state[-1][-1]) == sorted(goalPos): # all boxes on goal, end search
            print(str(len(strategy[1:])) + ' ' + ','.join(strategy[1:]).replace(',',' ')) #output format: length L U U D ...
            break
        if state[-1] not in exploredSet:  #detect duplicate
            exploredSet.add(state[-1])
            cost = len([x for x in strategy[1:]]) 
            for move in nextMove(state[-1][0], state[-1][1]): #try different correct moves
                newPlayerPos, newBoxPos = updateState(state[-1][0], state[-1][1], move) #update the states
                h = heuristic(newPlayerPos, newBoxPos)
                step += 1
                heapq.heappush(frontier, (h + cost, step, [(newPlayerPos, newBoxPos)])) #push new state into priority queue
                heapq.heappush(moves, (h + cost, step, strategy + [move[-1]]))


if __name__ == '__main__':
    start = time.time()
    wallPos, boxPos, goalPos, playerPos = generateGameMap(sys.argv[1]) #initialize the positions
    aStarSearch()
    end = time.time()
    runtime = start - end
    print('Runtime of ' + sys.argv[1] + ' using astar algorithm: %.2f second.' %runtime) #print runtime