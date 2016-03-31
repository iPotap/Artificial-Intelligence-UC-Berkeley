# search.py
# ---------
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

#All the collection types have the necessary push (INSERT) and pop (REMOVE-FRONT) and isEmpty methods to implement the above pseudo code.
#The problem object passed in to the depthFirstSearch function provide the other functions getSuccessors (EXPAND) and isGoalState (GOAL-TEST)
#Hopefully this helps you get started.
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from time import sleep
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    state = problem.getStartState()
    visited = set()    
    fringe = util.Stack()
    visited.add(state) 
    previous_actions = []
    for next_state, action, cost in problem.getSuccessors(state):
                fringe.push((next_state, [action]))
    
    while not problem.isGoalState(state):
        if fringe.isEmpty():
            previous_actions = []
            print "Oh no"
            return previous_actions

        next_state, previous_actions = fringe.pop()
        state = next_state
        
        if problem.isGoalState(next_state):            
            return previous_actions              
        
        if next_state not in visited:            
            visited.add(next_state)

            for next_state, action, cost in problem.getSuccessors(state):
                fringe.push((next_state, previous_actions + [action]))

    return previous_actions        
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    state = problem.getStartState()
    visited = []    
    fringe = util.Queue()
    visited.append(state) 
    previous_actions = []
    for next_state, action, cost in problem.getSuccessors(state):
                fringe.push((next_state, [action]))
    
    while not problem.isGoalState(state):
        if fringe.isEmpty():
            previous_actions = []
            print "Oh no"
            return previous_actions

        next_state, previous_actions = fringe.pop()
        state = next_state
        
        if problem.isGoalState(next_state):            
            return previous_actions              
        
        if next_state not in visited:            
            visited.append(next_state)

            for next_state, action, cost in problem.getSuccessors(state):
                fringe.push((next_state, previous_actions + [action]))

    return previous_actions   
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    state = problem.getStartState()
    visited = set()    
    fringe = util.PriorityQueue()
    visited.add(state) 
    previous_actions = []
    costs = {problem.getStartState(): 0}

    for next_state, action, cost in problem.getSuccessors(state):
                fringe.push((next_state, [action],cost), cost)
    
    while not problem.isGoalState(state):
        if fringe.isEmpty():
            previous_actions = []
            print "Oh no"
            return previous_actions
        next_state, previous_actions, cost = fringe.pop()
        state = next_state
        costs[state] = cost

        if problem.isGoalState(next_state):      
            return previous_actions              
        
        if next_state not in visited:            
            visited.add(next_state)

            for next_state, action, cost in problem.getSuccessors(state):
                updatedCost = costs[state] + cost
                
                if next_state not in costs or updatedCost < costs[next_state]:
                    costs[next_state] = updatedCost
                    fringe.push((next_state, previous_actions + [action], updatedCost), updatedCost)

    return previous_actions   
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    state = problem.getStartState()
    visited = []    
    fringe = util.PriorityQueue()
    visited.append(state) 
    previous_actions = []

    
    for next_state, action, cost in problem.getSuccessors(state):
        fringe.push((next_state, [action], cost), cost + heuristic(next_state, problem))
    
    while not problem.isGoalState(state):
        if fringe.isEmpty():
            previous_actions = []
            print "Oh no"
            return previous_actions
            
        next_state, previous_actions, cost = fringe.pop()
        state = next_state
        
        if problem.isGoalState(next_state):        
            return previous_actions              
        if next_state not in visited:            
            visited.append(next_state)   
            for next_state, action, cost in problem.getSuccessors(state):
                
                updatedCost = problem.getCostOfActions(previous_actions + [action])
                fringe.push((next_state, previous_actions + [action], updatedCost), updatedCost + heuristic(next_state, problem))

    return previous_actions   
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
