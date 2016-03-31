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
from random import randint

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
        legalMoves.remove('Stop');
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        justIndices = [index for index in range(len(scores))]
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        Pos = currentGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        distance_to_food = 9999
        distance_to_ghost = 9999

        foodList = newFood.asList()
        for food in foodList:
            if manhattanDistance(newPos, food) < distance_to_food:
                distance_to_food = manhattanDistance(newPos, food)


        for newGhostState in newGhostStates:
            if manhattanDistance(newPos, newGhostState.getPosition()) < distance_to_ghost:
                distance_to_ghost = manhattanDistance(newPos, newGhostState.getPosition())
            
        extra_food = 0 
        if newFood[newPos[0]][newPos[1]]:
            extra_food = 1
            
        if distance_to_ghost > 5:
            distance_to_ghost = 5
            
        if newGhostState.scaredTimer > 0:
            distance_to_ghost = 0
            
        Eval = 10/(distance_to_food) + distance_to_ghost + extra_food + successorGameState.getScore()
        
        return Eval
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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        return self.max_value(gameState, 1, 0)

    def min_value(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
            
        v = 9999
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            #if this is the last ghost
            if agentIndex == gameState.getNumAgents() - 1:
                #if we are at our depth limit
                if depth == self.depth:
                    temp_v = self.evaluationFunction(successor)
                else:
                    #maximize
                    temp_v = self.max_value(successor, depth + 1, 0)
            #if ghost was not the last one 
            else:
                temp_v = self.min_value(successor, depth, agentIndex + 1)

            if temp_v < v:
                v = temp_v 
                #minAction = action
                
        return v                
                
    
    def max_value(self, gameState, depth, agentIndex):        
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
            
        v = -9999
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
        
            #calling ghosts
            temp_v = self.min_value(successor, depth, 1)
            if temp_v > v:
                v = temp_v
                maxAction = action
        
            #if this is the first depth return ACTION to take, if not - number         
        if depth == 1:
            return maxAction
        else:
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
        return self.max_value(gameState, 1, 0, -9999, +9999)

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
            
        v = 9999
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            #if this is the last ghost
            if agentIndex == gameState.getNumAgents() - 1:
                #if we are at our depth limit
                if depth == self.depth:
                    temp_v = self.evaluationFunction(successor)
                else:
                    #maximize
                    temp_v = self.max_value(successor, depth + 1, 0, alpha, beta)
            #if ghost was not the last one 
            else:
                temp_v = self.min_value(successor, depth, agentIndex + 1, alpha, beta)
            
            if temp_v < v:
                v = temp_v 
                #minAction = action
                        
            if v < alpha:
                return v
            if v < beta:
                beta = v
                
        return v                
                
    
    def max_value(self, gameState, depth, agentIndex, alpha, beta):        
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
            
        v = -9999
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
        
            #calling ghosts
            temp_v = self.min_value(successor, depth, 1, alpha, beta)
            if temp_v > v:
                v = temp_v
                maxAction = action
            
            if v > beta:
                return v
            if v > alpha:
                alpha = v                
            
            #if this is the first depth return ACTION to take, if not - number         
        if depth == 1:
            return maxAction
        else:
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
        return self.max_value(gameState, 1, 0)

    def expect_value(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
         
        count = 0.0        
        v = 0.0
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            #if this is the last ghost
            if agentIndex == gameState.getNumAgents() - 1:
                #if we are at our depth limit
                if depth == self.depth:
                    temp_v = self.evaluationFunction(successor)
                else:
                    #maximize
                    temp_v = self.max_value(successor, depth + 1, 0)
            #if ghost was not the last one 
            else:
                temp_v = self.expect_value(successor, depth, agentIndex + 1)
                
            v = temp_v + v
            count = count + 1.0

        v = v / count   
        return v                
                
    
    def max_value(self, gameState, depth, agentIndex):        
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
            
        v = float('-inf')
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
        
            #calling ghosts
            temp_v = self.expect_value(successor, depth, 1)
            if temp_v > v:
                v = temp_v
                maxAction = action
        
            #if this is the first depth return ACTION to take, if not - number         
        if depth == 1:
            return maxAction
        else:
            return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    distance_to_food = 9999
    distance_to_ghost = 9999
    rand = 0 
    
    foodList = Food.asList()
    for food in foodList:
        if manhattanDistance(Pos, food) < distance_to_food:
            distance_to_food = manhattanDistance(Pos, food)


    for GhostState in GhostStates:
        if manhattanDistance(Pos, GhostState.getPosition()) < distance_to_ghost:
            distance_to_ghost = manhattanDistance(Pos, GhostState.getPosition())
            
    extra_food = 0 
    if Food[Pos[0]][Pos[1]]:
        extra_food = 1
            
    if distance_to_ghost > 3:
        distance_to_ghost = 3
        rand = randint(2,5)
            
    if GhostState.scaredTimer > 0:
        distance_to_ghost = 0
            
    Eval = 1000/(distance_to_food) + distance_to_ghost/10 + extra_food*1000 + currentGameState.getScore()*1000 + rand
        
    return Eval

# Abbreviation
better = betterEvaluationFunction

