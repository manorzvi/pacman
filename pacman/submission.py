import random
import util
from game import Agent
import numpy as np
import math


#     ********* Reflex agent- sections a and b *********
class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None

  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()
    #print(legalMoves)
    # Choose one of the best actions
    move_score_pairs = {action : self.evaluationFunction(gameState, action) for action in legalMoves}
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    #print('move-score pairs:', end=' ');print(move_score_pairs)
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    #print('Chosen Move:',end=' ');print(legalMoves[chosenIndex])
    #input('Press <ENTER> to continue')
    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current GameState (pacman.py) and the proposed action
    and returns a number, where higher numbers are better.
    """
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    #return scoreEvaluationFunction(successorGameState)

    return betterEvaluationFunction(successorGameState)

#     ********* Evaluation functions *********

def scoreEvaluationFunction(gameState):
  """"
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
  """
  return gameState.getScore()

######################################################################################
# b: implementing a better heuristic function
def betterEvaluationFunction(gameState):
  """

  The betterEvaluationFunction takes in a GameState (pacman.py) and should return a number, where higher numbers are better.

  A GameState specifies the full game state, including the food, capsules, agent configurations and more.
  Following are a few of the helper methods that you can use to query a GameState object to gather information about
  the present state of Pac-Man, the ghosts and the maze:

  gameState.getLegalActions():
  gameState.getPacmanState():
  gameState.getGhostStates():
  gameState.getNumAgents():
  gameState.getScore():
  The GameState class is defined in pacman.py and you might want to look into that for other helper methods.
  """
  if gameState.isLose():
      return float(-np.inf)
  elif gameState.isWin():
      return float(np.inf)


  minDistFood = getMinDistFood(gameState)
  #print(getMinDistFood(gameState))


  #score = gameState.getScore() + 1/minDistFood
  score = gameState.getScore() - minDistFood # the smaller minDistFood, the better
  score -= gameState.getNumFood()

  goodGhosts = list()
  badGhosts = list()
  for ghost in gameState.getGhostStates():
      if ghost.scaredTimer:
          goodGhosts.append(ghost)
      else:
          badGhosts.append(ghost)

  pos = gameState.getPacmanPosition()

  #minDistBadGhost = getMinDistGhost(pos,badGhosts)
  #score += 2*minDistBadGhost # we like bad ghosts as far as possible

  #minDistGoodGhost = getMinDistGhost(pos,goodGhosts)
  #score -= 2*minDistGoodGhost # the closer good ghost is the better

  numCapsule = getNumCaspsules(gameState)
  #print(numCapsule)
  score -= numCapsule # if capsules number in next state lower then current, it means that we have ate a capsule.
                            # which is good.

  if isCapsule(pos,gameState):
      return np.inf

  #if isBadGhost(pos,badGhosts):
  #    return -np.inf

  score -= 10*len(badGhosts)

  return score

def isBadGhost(pos,badGhosts):
    for g in badGhosts:
        if g.getPosition() == pos:
            return True
        else:
            return False



def isCapsule(pos,gameState):
    capsulesPos = gameState.getCapsules()
    for c in capsulesPos:
        if pos == c:
            return True
        else:
            return False


def getNumCaspsules(gameState):
    return len(gameState.getCapsules())

def getMinDistGhost(pos,Ghosts):

    ghostsPositions = [g.getPosition() for g in Ghosts]
    if ghostsPositions:
        return min(map(lambda x: util.manhattanDistance(pos, x), ghostsPositions))
    else:
        return 0


def getMinDistFood(gameState):
    """
    gameState: GameState object of current state inspected
    return   : the minimal distance to food from current pacman location
    """

    foodGrid = gameState.getFood()
    foodList = foodGrid.asList()

    pos = gameState.getPacmanPosition()

    minDistFood = min(map(lambda x: util.manhattanDistance(pos, x), foodList))
    return minDistFood

#     ********* MultiAgent Search Agents- sections c,d,e,f*********


class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxAgent, AlphaBetaAgent & both ExpectimaxAgents.

    You  *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# c: implementing minimax


class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following:
      pacman won, pacman lost or there are no legal moves.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game

      gameState.isWin():
        Returns True if it's a winning state

      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue
    """
    minimax = -math.inf
    minimax_action = []
    agent = self.index
    for action in gameState.getLegalActions(agent):
        curr_minimax = self.minimax(gameState.generateSuccessor(agent, action), agent, self.depth)
        if curr_minimax >= minimax:
            minimax = curr_minimax
            minimax_action = action
    return minimax_action

  def minimax(self, gameState, agent, depth):
    if agent >= gameState.getNumAgents():
        agent = 0
        depth -= 1
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

    children = list()
    for action in gameState.getLegalActions(agent):
        children.append(gameState.generateSuccessor(agent, action))

    if agent == 0:
        cur_max = -math.inf
        for c in children:
            v = self.minimax(c, agent+1, depth)
            cur_max = max(cur_max, v)
        return cur_max

    else:
        cur_min = math.inf
        for c in children:
            v = self.minimax(c, agent+1, depth)
            cur_min = min(cur_min, v)
        return cur_min

######################################################################################
# d: implementing alpha-beta


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    minimax = -math.inf
    minimax_action = []
    turn = self.index
    for action in gameState.getLegalActions(turn):
        curr_minimax = self.alpha_beta(gameState.generateSuccessor(turn, action), turn, self.depth, -math.inf, math.inf)
        if curr_minimax > minimax:
            minimax = curr_minimax
            minimax_action = action
    return minimax_action

  def alpha_beta(self, gameState, agent, depth, alpha, beta):
    if agent >= gameState.getNumAgents():
        agent = 0
        depth -= 1
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

    children = list()
    turn = self.index
    for action in gameState.getLegalActions(turn):
        children.append(gameState.generateSuccessor(turn, action))

    if turn == 0:
        cur_max = -math.inf
        for c in children:
            v = self.alpha_beta(c, agent+1, depth, alpha, beta)
            cur_max = max(cur_max, v)
            alpha = max(cur_max, alpha)
            if cur_max >= beta:
                return math.inf
        return cur_max

    else:
        cur_min = math.inf
        for c in children:
            v = self.alpha_beta(c, agent+1, depth, alpha, beta)
            cur_min = min(cur_min, v)
            beta = min(cur_min, beta)
            if cur_min <= alpha:
                return -math.inf
        return cur_min

######################################################################################
# e: implementing random expectimax

class RandomExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction
      All ghosts should be modeled as choosing uniformly at random from their legal moves.
    """

    # BEGIN_YOUR_CODE
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

######################################################################################
# f: implementing directional expectimax

class DirectionalExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction
      All ghosts should be modeled as using the DirectionalGhost distribution to choose from their legal moves.
    """

    # BEGIN_YOUR_CODE
    raise Exception("Not implemented yet")
    # END_YOUR_CODE


######################################################################################
# I: implementing competition agent

class CompetitionAgent(MultiAgentSearchAgent):
  """
    Your competition agent
  """

  def getAction(self, gameState):
    """
      Returns the action using self.depth and self.evaluationFunction

    """

    # BEGIN_YOUR_CODE
    raise Exception("Not implemented yet")
    # END_YOUR_CODE



