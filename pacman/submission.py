import random
import util
from game import Agent
from game import Actions
import math

#     ********* Original Reflex agent- section h *********
class OriginalReflexAgent(Agent):
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

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]

    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current GameState (pacman.py) and the proposed action
    and returns a number, where higher numbers are better.
    """
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    return scoreEvaluationFunction(successorGameState)


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

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]

    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current GameState (pacman.py) and the proposed action
    and returns a number, where higher numbers are better.
    """
    successorGameState = currentGameState.generatePacmanSuccessor(action)

    return betterEvaluationFunction(successorGameState)


#     ********* Evaluation functions *********
def scoreEvaluationFunction(gameState):
  """"
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
  """
  return gameState.getScore()


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

  #if gameState.isWin():
  #    return 10000
  if gameState.isLose():
      return -10000

  pos = gameState.getPacmanPosition()
  minDistFood = getMinDistFood(gameState, pos)
  #print(getMinDistFood(gameState))

  # the smaller minDistFood, the better
  score = gameState.getScore() + 1/minDistFood

  goodGhosts = list()
  badGhosts = list()
  for ghost in gameState.getGhostStates():
      if ghost.scaredTimer:
          goodGhosts.append(ghost)
      else:
          badGhosts.append(ghost)


  minDistBadGhost = getMinDistGhost(pos,badGhosts)
  if minDistBadGhost > 0:
       score -= 1/minDistBadGhost # we like bad ghosts as far as possible

  minDistGoodGhost = getMinDistGhost(pos,goodGhosts)
  if minDistGoodGhost > 0:
      score += 1/minDistGoodGhost # the closer good ghost is the better

  numCapsule = len(gameState.getCapsules())
  # if capsules number in next state lower then current, it means that we ate a capsule.
  # which is good.
  if numCapsule > 0:
      score += 1/numCapsule

  return score


def getMinDistGhost(pos,Ghosts):

    ghostsPositions = [g.getPosition() for g in Ghosts]
    if ghostsPositions:
        return min(map(lambda x: util.manhattanDistance(pos, x), ghostsPositions))
    else:
        return 0


def getMinDistFood(gameState, pos):
    """
    gameState: GameState object of current state inspected
    return   : the minimal distance to food from current pacman location
    """
    foodGrid = gameState.getFood()
    foodList = foodGrid.asList()

    if len(foodList)> 0 :
        minDistFood = min(map(lambda x: util.manhattanDistance(pos, x), foodList))
    else:
        return 1
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


# c: implementing Minimax
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
    minimax = self.minimax(gameState, self.index, self.depth)
    return minimax[1]

  def minimax(self, gameState, agent, depth):
    if agent >= gameState.getNumAgents():
        agent = 0
        depth -= 1
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return [self.evaluationFunction(gameState), []]

    if agent == 0:
        cur_max_v = -math.inf
        cur_action = []
        for action in gameState.getLegalActions(agent):
            c = gameState.generateSuccessor(agent, action)
            v = self.minimax(c, agent+1, depth)[0]
            if v >= cur_max_v:
                cur_max_v = v
                cur_action = action
        return [cur_max_v, cur_action]

    else:
        cur_min_v = math.inf
        cur_action = []
        for action in gameState.getLegalActions(agent):
            c = gameState.generateSuccessor(agent, action)
            v = self.minimax(c, agent+1, depth)[0]
            if v <= cur_min_v:
                cur_min_v = v
                cur_action = action
        return [cur_min_v, cur_action]


# d: implementing alpha-beta
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    alpha_beta = self.alpha_beta(gameState, self.index, self.depth, -math.inf, math.inf)
    return alpha_beta[1]

  def alpha_beta(self, gameState, agent, depth, alpha, beta):
    if agent >= gameState.getNumAgents():
        agent = 0
        depth -= 1
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return [self.evaluationFunction(gameState), []]

    if agent == 0:
        cur_max_v = -math.inf
        cur_action = []
        for action in gameState.getLegalActions(agent):
            c = gameState.generateSuccessor(agent, action)
            v = self.alpha_beta(c, agent+1, depth, alpha, beta)[0]
            if v >= cur_max_v:
                cur_max_v = v
                cur_action = action
            alpha = max(cur_max_v, alpha)
            if cur_max_v >= beta:
                return [math.inf, cur_action]
        return [cur_max_v, cur_action]

    else:
        cur_min_v = math.inf
        cur_action = []
        for action in gameState.getLegalActions(agent):
            c = gameState.generateSuccessor(agent, action)
            v = self.alpha_beta(c, agent+1, depth, alpha, beta)[0]
            if v <= cur_min_v:
                cur_min_v = v
                cur_action = action
            beta = min(cur_min_v, beta)
            if cur_min_v <= alpha:
                return [-math.inf, cur_action]
        return [cur_min_v, cur_action]


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
    random_expectimax = self.random_expectimax(gameState, self.index, self.depth)
    return random_expectimax[1]

  def random_expectimax(self, gameState, agent, depth):
    if agent >= gameState.getNumAgents():
        agent = 0
        depth -= 1
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return [self.evaluationFunction(gameState), []]

    if agent == 0:
        cur_max_v = -math.inf
        cur_action = []
        for action in gameState.getLegalActions(agent):
            c = gameState.generateSuccessor(agent, action)
            v = self.random_expectimax(c, agent + 1, depth)[0]
            if v >= cur_max_v:
                cur_max_v = v
                cur_action = action
        return [cur_max_v, cur_action]

    else:
        action = []
        p = 1.0/float(len(gameState.getLegalActions(agent)))
        v = 0
        for action in gameState.getLegalActions(agent):
            c = gameState.generateSuccessor(agent, action)
            v += p * self.random_expectimax(c, agent + 1, depth)[0]
        return [v, action]


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

    dir_random_expectimax = self.directional_random_expectimax(gameState, self.index, self.depth)
    return dir_random_expectimax[1]

  def directional_random_expectimax(self, gameState, agent, depth):

      if agent >= gameState.getNumAgents():
          agent = 0
          depth -= 1
      if gameState.isWin() or gameState.isLose() or depth == 0:
          return [self.evaluationFunction(gameState), []]

      if agent == 0:
          cur_max_v = -math.inf
          cur_action = []
          for action in gameState.getLegalActions(agent):
              c = gameState.generateSuccessor(agent, action)
              v = self.directional_random_expectimax(c, agent + 1, depth)[0]
              if v >= cur_max_v:
                  cur_max_v = v
                  cur_action = action
          return [cur_max_v, cur_action]


      else:
          action = []
          dist = getDistribution(gameState, agent)
          v = 0
          for action,prob in dist.items():
              c = gameState.generateSuccessor(agent, action)
              v += prob * self.directional_random_expectimax(c, agent + 1, depth)[0]
          return [v, action]


def getDistribution(gameState, agent):
    ghostState = gameState.getGhostState(agent)
    legalActions = gameState.getLegalActions(agent)
    pos = gameState.getGhostPosition(agent)
    isScared = ghostState.scaredTimer > 0

    speed = 1
    if isScared: speed = 0.5

    actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
    newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
    pacmanPosition = gameState.getPacmanPosition()

    # Select best actions given the state
    distancesToPacman = [util.manhattanDistance(pos, pacmanPosition) for pos in newPositions]
    if isScared:
        bestScore = max(distancesToPacman)
        bestProb = 0.8
    else:
        bestScore = min(distancesToPacman)
        bestProb = 0.8

    bestActions = [action for action, distance in zip(legalActions, distancesToPacman) if distance == bestScore]
    # print('best actions:',end=' ');print(bestActions)

    # Construct distribution
    dist = util.Counter()
    for a in bestActions: dist[a] = bestProb / len(bestActions)
    # print('1) dist:',end=' ');print(dist)
    for a in legalActions: dist[a] += (1 - bestProb) / len(legalActions)
    # print('2) dist:',end=' ');print(dist)
    dist.normalize()
    #print('3) dist:',end=' ');print(dist)
    return dist


# I: implementing competition agent
class CompetitionAgent(MultiAgentSearchAgent):
  """
    Your competition agent
  """
  def getAction(self, gameState):
    competition = self.competition(gameState, self.index, 3, -math.inf, math.inf)
    return competition[1]

  def competition(self, gameState, agent, depth, alpha, beta):
    if agent >= gameState.getNumAgents():
        agent = 0
        depth -= 1
    if gameState.isWin() or gameState.isLose() or depth == 0:
        return [self.evaluationFunction(gameState), []]

    if agent == 0:
        cur_max_v = -math.inf
        cur_action = []
        for action in gameState.getLegalActions(agent):
            c = gameState.generateSuccessor(agent, action)
            v = self.competition(c, agent+1, depth, alpha, beta)[0]
            if v >= cur_max_v:
                cur_max_v = v
                cur_action = action
            alpha = max(cur_max_v, alpha)
            if cur_max_v >= beta:
                return [math.inf, cur_action]
        return [cur_max_v, cur_action]

    else:
        cur_min_v = math.inf
        cur_action = []
        for action in gameState.getLegalActions(agent):
            c = gameState.generateSuccessor(agent, action)
            v = self.competition(c, agent+1, depth, alpha, beta)[0]
            if v <= cur_min_v:
                cur_min_v = v
                cur_action = action
            beta = min(cur_min_v, beta)
            if cur_min_v <= alpha:
                return [-math.inf, cur_action]
        return [cur_min_v, cur_action]


