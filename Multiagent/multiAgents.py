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
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

