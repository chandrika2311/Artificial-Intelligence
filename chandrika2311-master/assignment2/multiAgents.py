# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    alreadyBeenHere = []
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        print "Scores:",scores
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]

        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        print"Chosen Index", chosenIndex
        "Add more of your code here if you want to"
        
        self.alreadyBeenHere.append(chosenIndex)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        

        
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        Score = successorGameState.getScore()
        

        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        ""
        "*** YOUR CODE HERE ***"
        #Begin of Changes by Chandrika
        #if newPos in self.alreadyBeenHere:
        #	Score += 40
        
        newGhostPositions = successorGameState.getGhostPositions()
        #if newPos in newGhostPositions:
        #	Score += 200
        
        newFoodPositions = successorGameState.getFood().asList()
        
		
        distancesFromGhost = [manhattanDistance(newPos , g ) for g in newGhostPositions]
        if len(distancesFromGhost)> 0:
        	GhostScore = min(distancesFromGhost)
        	
        	
        	#if distanceFromGhost <= 1:
        	#	Score += 300
        	#else:
        	#	Score += max(distanceFromGhost, 3)
        		
        #if action == Directions.STOP:
		#	Score += 50	
        #if (currentGameState.getNumFood() > successorGameState.getNumFood()):
		#	Score -=300
		
		distancesFromFood = [ manhattanDistance(newPos , f ) for f in newFoodPositions]
		if len(distancesFromFood)> 0:	
			FoodScore = min(distancesFromFood)
			#if distanceFromFood == 0 :
			#	Score-= 1000
			#elif distanceFromFood <= 1:
			#	Score-= 500
			#else:
			Score+= GhostScore/FoodScore
        return Score
        #return successorGameState.getScore()
      
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
      

    

    	

	

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    #Begin Of change by Chandrika
    def getAction(self, gameState):
    	def maxValue(state, CurrentNodeDepth):
    		CurrentNodeDepth = CurrentNodeDepth + 1
    		if state.isWin() or state.isLose() or CurrentNodeDepth == self.depth:
    			return self.evaluationFunction(state)
    		value = float('-Inf')
    		for Action in state.getLegalActions(0):
    			value = max(value, minValue(state.generateSuccessor(0, Action), CurrentNodeDepth, 1))
    		return value

    	def terminalTest(state, curdepth):
    		if state.isWin() or state.isLose() or curdepth == self.depth:
    			return True
    		else:
    			return False

    	def minValue(state, CurrentNodeDepth, CurghostNumber):
    		if state.isWin() or state.isLose():
    			return self.evaluationFunction(state)
    		value = float('Inf')
    		for pAction in state.getLegalActions(CurghostNumber):
    			if CurghostNumber == gameState.getNumAgents() - 1:
    				value = min(value, maxValue(state.generateSuccessor(CurghostNumber, pAction), CurrentNodeDepth))
        		else:
        			nextGhostNumber=CurghostNumber+1
          			value = min(value, minValue(state.generateSuccessor(CurghostNumber, pAction), CurrentNodeDepth, nextGhostNumber))
      		return value
      				
    	def utility(state):
    		return self.evaluationFunction(state)	

    	def res(state,agentIndex, action):
    		return state.generateSuccessor(agentIndex,action)			
        

        		
       	#Letting the pacman start first:
    	pacmanActions = gameState.getLegalActions(0)
    	maximum = float('-Inf')
    	maximizingAction = ''
    	for action in pacmanActions:
      		CurrentNodeDepth = 0
      		currentMaxizer = minValue(gameState.generateSuccessor(0, action), CurrentNodeDepth, 1)
      		if currentMaxizer > maximum:
        		maximum = currentMaxizer
        		maximizingAction = action
    	return maximizingAction
		#End Of change by Chandrika

        # returns a utility value
    	"*** YOUR CODE HERE ***"
    	util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def minValue(self,state, CurrentNodeDepth,alpha, beta, CurrentghostNumber):
    		if state.isWin() or state.isLose():
    			return self.evaluationFunction(state)
    		value = float('Inf')
    		for Action in state.getLegalActions(CurrentghostNumber):
    			if CurrentghostNumber == state.getNumAgents() - 1:
    				
    				value = min(value, self.maxValue(state.generateSuccessor(CurrentghostNumber, Action),CurrentNodeDepth,alpha, beta))
        		else:
        			nextGhostNumber=CurrentghostNumber+1
          			value = min(value, self.minValue(state.generateSuccessor(CurrentghostNumber, Action),CurrentNodeDepth, alpha, beta, nextGhostNumber))
          		if value < alpha:
          			return value
          		beta = min(beta,value)	
      		
      		return value
    def maxValue(self,state,CurrentNodeDepth, alpha, beta ):
    			CurrentNodeDepth = CurrentNodeDepth + 1
    			if state.isWin() or state.isLose() or CurrentNodeDepth == self.depth:
    				return self.evaluationFunction(state)
    			value = float('-Inf')
    			for Action in state.getLegalActions(0):
    				value = max(value, self.minValue(state.generateSuccessor(0, Action), CurrentNodeDepth, alpha, beta, 1))
    				if value > beta:
    					return value
    				alpha = max(alpha,value)	
    		
    			return value  		
    def getAction(self, gameState):

    	pacmanActions = gameState.getLegalActions(0)
    	
    	alpha = float('-Inf')
    	beta = float('Inf')
    	maximizingAction = ''
    	for action in pacmanActions:
      		CurrentNodeDepth = 0
      		currentMaxizer = self.minValue(gameState.generateSuccessor(0, action),CurrentNodeDepth,alpha,beta, 1)
      		if currentMaxizer > alpha:
        		alpha = currentMaxizer
        		maximizingAction = action
    	return maximizingAction

    	util.raiseNotDefined()
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """"""
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
    "*** YOUR CODE HERE ***"
    def expectiValue(self,state, CurrentNodeDepth,CurrentghostNumber):
    	if state.isWin() or state.isLose():
    		return self.evaluationFunction(state)
    	value = 0
     	for Action in state.getLegalActions(CurrentghostNumber):
    		if CurrentghostNumber == state.getNumAgents() - 1:
    			value = value + (self.maxValue(state.generateSuccessor(CurrentghostNumber, Action),CurrentNodeDepth)/len(state.getLegalActions(CurrentghostNumber)))
        	else:
        		nextGhostNumber=CurrentghostNumber+1
          		value = value + (self.expectiValue(state.generateSuccessor(CurrentghostNumber, Action),CurrentNodeDepth, nextGhostNumber)/len(state.getLegalActions(CurrentghostNumber)))      		
      	return value
    def maxValue(self,state,CurrentNodeDepth):
    	CurrentNodeDepth = CurrentNodeDepth + 1
    	if state.isWin() or state.isLose() or CurrentNodeDepth == self.depth:
    		return self.evaluationFunction(state)
    	value = float('-Inf')
    	for Action in state.getLegalActions(0):
    		value = max(value, self.expectiValue(state.generateSuccessor(0, Action), CurrentNodeDepth,1))
    	return value  	

    def getAction(self, gameState):
    	pacmanActions = gameState.getLegalActions(0)
    	maximizingAction = ''
    	maximum = 0
    	for action in pacmanActions:
      		CurrentNodeDepth = 0
      		currentMaxizer = self.expectiValue(gameState.generateSuccessor(0, action),CurrentNodeDepth,1)
      		if currentMaxizer > maximum:
        		maximizingAction = action
        		maximum = currentMaxizer
        		
    	return maximizingAction

    	util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
	#Begin of Changes by Chandrika
    
    Score = currentGameState.getScore()
        

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newGhostPositions = currentGameState.getGhostPositions()
    newFoodPositions = currentGameState.getFood().asList()
    """	
    if sum(newScaredTimes) > 2 :
    	for ghostDistance in distancesFromGhost:
    		if ghostDistance < 2:
    			safe_factor += 0.4
    		if ghostDistance < 3:
    			safe_factor+= 0.2
    		if ghostDistance < 4:
    			safe_factor += 0.1
    else:
    	for ghostDistance in distancesFromGhost:
    		if ghostDistance < 2:
    			safe_factor -= 0.4
    		if ghostDistance < 3:
    			safe_factor -= 0.2
    		if ghostDistance < 4:
    			safe_factor -= 0.1
    """
    distancesFromGhost = [manhattanDistance(newPos , g ) for g in newGhostPositions]
    if len(distancesFromGhost)> 0:
    	GhostScore = min(distancesFromGhost)
    distancesFromFood = [ manhattanDistance(newPos , f ) for f in newFoodPositions]
    if len(distancesFromFood)> 0:
    	FoodScore = min(distancesFromFood)
    	Score+= GhostScore/FoodScore*6
        

		#Safe situations:
	


    return Score
    util.raiseNotDefined()


better = betterEvaluationFunction

