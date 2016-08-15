# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

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
        "*** YOUR CODE HERE ***"
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        curPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()

        curFood = currentGameState.getFood()
        curFoodList = curFood.asList()
        newFood = successorGameState.getFood()
        newFoodList = newFood.asList()

        currCapsules = currentGameState.getCapsules()
        newCapsules = successorGameState.getCapsules()
        
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ghostPositions = successorGameState.getGhostPositions()
        
        distance2Ghost = float("inf")
        scared = min(newScaredTimes)
        
        for ghost in ghostPositions:
          d = manhattanDistance(ghost, newPos)
          distance2Ghost = min(d, distance2Ghost)
        
        distance2FoodMin = float("inf")        
        distance2FoodMax = float("-inf")
        distance2Cap = float("inf")
        flagMin = 0
        flagMax = 0
        flagCap = 0
        for food in newFoodList:
          d = manhattanDistance(food, newPos)
          if d<distance2FoodMin and d > 0:
            distance2FoodMin = d
            minPos = food
            flagMin = 1

        if flagMin == 1:
          for food in newFoodList:  
            d = manhattanDistance(food, minPos)
            if d > distance2FoodMax and d > 0:
              distance2FoodMax = d
              flagMax = 1

        for cap in newCapsules:
          d = manhattanDistance(cap, newPos)
          if d < distance2Cap and d > 0:
            distance2Cap = d
            flagCap = 1

        #foodLeft = len(newFoodList)
        #foodLeft is a dumb factor
        foodEaten = 0
        if len(newFoodList) < len(curFoodList):
          foodEaten = 10000

        capsuleEaten = 0
        if len(newCapsules) < len(currCapsules):
          capsuleEaten = 10000
        
        ghostFactor = 0

        if distance2Ghost < 2:
          if scared < 2:
            ghostFactor = -100000
          else:
            ghostFactor = 10000

        #diff = currentGameState.getScore() - successorGameState.getScore()

        if flagMin == 1 and flagMax == 1 and flagCap == 1:
          return distance2Ghost + 1000.0/distance2FoodMin + 1000.0/distance2FoodMax + 1000.0/distance2Cap + foodEaten + capsuleEaten + ghostFactor
        elif flagMin == 1 and flagCap == 1:
          return distance2Ghost + 1000.0/distance2FoodMin + 1000.0/distance2Cap + foodEaten + capsuleEaten + ghostFactor
        elif flagMin == 1:
          return distance2Ghost + 1000.0/distance2FoodMin + foodEaten + capsuleEaten + ghostFactor
        else:
          return distance2Ghost + foodEaten + capsuleEaten + ghostFactor

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

      def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = minimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)
            if temp > v:
              v = temp
              bestAction = successor[0]
        return bestAction
        
def minimax(agent, agentList, state, depth, evalFunc):
      
      # at Leaf
      if depth <= 0 or state.isWin() == True or state.isLose() == True:
        return evalFunc(state)
        
      if agent == 0:
        v = float("-inf")
      else:
        v = float("inf")
              
      actions = state.getLegalActions(agent)
      successors = [state.generateSuccessor(agent, action) for action in actions]
      for j in range(len(successors)):
        successor = successors[j]
        if agent == 0: 
          v = max(v, minimax(agentList[agent+1], agentList, successor, depth, evalFunc))
        elif agent == agentList[-1]:
          v = min(v, minimax(agentList[0], agentList, successor, depth - 1, evalFunc))
        else:
          v = min(v, minimax(agentList[agent+1], agentList, successor, depth, evalFunc))
      
      return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
      """
      Returns the minimax action using self.depth and self.evaluationFunction
      """
      "*** YOUR CODE HERE ***"
      v = float("-inf")
      alpha = float("-inf")
      beta = float("inf")
      bestAction = []
      agent = 0
      actions = gameState.getLegalActions(agent)
      successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
      for successor in successors:
        temp = minimaxPrune(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction, alpha, beta)
            
        if temp > v:
          v = temp
          bestAction = successor[0]
            
        if v > beta:
          return bestAction
            
        alpha = max(alpha, v)
        
      return bestAction
        
def minimaxPrune(agent, agentList, state, depth, evalFunc, alpha, beta):
  
      if depth <= 0 or state.isWin() == True or state.isLose() == True:
        return evalFunc(state)
    
      if agent == 0:
        v = float("-inf")
      else:
        v = float("inf")
          
      actions = state.getLegalActions(agent)
      for action in actions:
        successor = state.generateSuccessor(agent, action)
        
        if agent == 0:
          v = max(v, minimaxPrune(agentList[agent+1], agentList, successor, depth, evalFunc, alpha, beta))
          alpha = max(alpha, v)
          if v > beta:
            #print v
            return v
        
        elif agent == agentList[-1]:  
          v = min(v, minimaxPrune(agentList[0], agentList, successor, depth - 1, evalFunc, alpha, beta))
          beta = min(beta, v)
          if v < alpha:
            #print v
            return v
            
        else:
          v = min(v, minimaxPrune(agentList[agent+1], agentList, successor, depth, evalFunc, alpha, beta))
          beta = min(beta, v)
          if v < alpha:
            #print v
            return v

      return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = expectimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)
            if temp > v:
              v = temp
              bestAction = successor[0]
        return bestAction

def expectimax(agent, agentList, state, depth, evalFunc):
      
      # at Leaf
      if depth <= 0 or state.isWin() == True or state.isLose() == True:
        return evalFunc(state)
        
      if agent == 0:
        v = float("-inf")
      else:
        v = 0
              
      actions = state.getLegalActions(agent)
      successors = [state.generateSuccessor(agent, action) for action in actions]
      for successor in successors:
        if agent == 0: 
          v = max(v, expectimax(agentList[agent+1], agentList, successor, depth, evalFunc))
        elif agent == agentList[-1]:
          v = v + expectimax(agentList[0], agentList, successor, depth - 1, evalFunc)
        else:
          v = v + expectimax(agentList[agent+1], agentList, successor, depth, evalFunc)
      
      if agent == 0:
        return v
      else:
        return v/float(len(successors))

def betterEvaluationFunction(currentGameState):
        """
          Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
          evaluation function (question 5).

          DESCRIPTION: <write something here so we know what you did>
        """
        "*** YOUR CODE HERE ***"
        currPos = currentGameState.getPacmanPosition()
        currFood = currentGameState.getFood()
        currFoodList = currFood.asList()
        currCapsules = currentGameState.getCapsules()
        currGhostStates = currentGameState.getGhostStates()
        scaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates]
        ghostPositions = currentGameState.getGhostPositions()
        
        distance2Ghost = float("inf")
        
        scared = min(scaredTimes)
        
        for ghost in ghostPositions:
          d = manhattanDistance(ghost, currPos)
          distance2Ghost = min(d, distance2Ghost)
        
        distance2FoodMin = float("inf")        
        distance2FoodMax = float("-inf")
        distance2Cap = float("inf")
        flagMin = 0
        flagMax = 0
        flagCap = 0
        for food in currFoodList:
          d = manhattanDistance(food, currPos)
          if d<distance2FoodMin and d > 0:
            distance2FoodMin = d
            minPos = food
            flagMin = 1

        if flagMin == 1:
          for food in currFoodList:  
            d = manhattanDistance(food, minPos)
            if d > distance2FoodMax and d > 0:
              distance2FoodMax = d
              flagMax = 1

        for cap in currCapsules:
          d = manhattanDistance(cap, currPos)
          if d < distance2Cap and d > 0:
            distance2Cap = d
            flagCap = 1

        foodLeft = float(len(currFoodList))
        if foodLeft > 0:
          flagFood = 1
        else:
          flagFood = 0
        
        ghostFactor = 0
        if distance2Ghost < 2:
          if scared < 2:
            ghostFactor = -100000
          else:
            ghostFactor = 10000

        score = currentGameState.getScore()
        if currentGameState.isWin():
          #print "hiiii"
          return 1000000

        #diff = currentGameState.getScore() - successorGameState.getScore()
        
        if flagMin == 1 and flagMax == 1 and flagCap == 1:
          return distance2Ghost + 100.0/distance2FoodMin + 1.0/distance2FoodMax + 1.0/distance2Cap + 10000.0/foodLeft + ghostFactor + 10*score
        elif flagMin == 1 and flagMax == 1:
          return distance2Ghost + 100.0/distance2FoodMin + 1.0/distance2FoodMax + 10000.0/foodLeft + ghostFactor + 10*score
        elif flagMin == 1 and flagCap == 1:
          #len(currFoodList) is always 1
          #print distance2Ghost + 100.0/distance2FoodMin + 10000.0/foodLeft + ghostFactor + 10*score
          return distance2Ghost + 100.0/distance2FoodMin + 10000.0/foodLeft + ghostFactor + 10*score
        elif flagMin == 1:
          #len(currFoodList) is always 1
          return distance2Ghost + 100.0/distance2FoodMin + 10000.0/foodLeft + ghostFactor + 10*score
        
# Abbreviation
better = betterEvaluationFunction

