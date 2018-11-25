# contains random agent, qlearning agent, approximate qlearning agent
import random, util
from featureExtractor import *

class RLAgent:
    def __init__(self, numTraining=10, numTesting=10, gamesPerEpisode=10, epsilon=0.5, alpha=0.5, gamma=1, values=None):
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.numTraining = int(numTraining)
        self.numTesting = int(numTesting)
        self.gamesPerEpisode = int(gamesPerEpisode)
        self.episodesSoFar = 0
        self.gamesSoFar = 0
        self.episodeRewards = 0.0
        self.values = values

    def update(self, state, action, nextState, reward, legalActions):
        pass

    def stateExtractor(self, board, currentPiece, nextPiece):
        return (board.board, currentPiece.shape, nextPiece.shape)

    def observeTransition(self, state, action, nextState, reward, legalActions):
        self.episodeRewards += reward
        self.update(state, action, nextState, reward, legalActions)

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return self.episodesSoFar < self.numTesting

    def startEpisode(self):
        """
          Called by environment when new episode of games is starting
        """
        self.episodeRewards = 0.0

    def shouldStopEpisode(self):
        """
        Called by environment to check that we are finished with an episode
        """
        return (self.gamesSoFar != 0) and (self.gamesSoFar % self.gamesPerEpisode == 0)

    def stopEpisode(self):
        """
          Called by environment when episode is done
        """
        self.episodesSoFar += 1

    def recordGame(self):
        """
        Called by environment to record that we have just finished playing a game of tetris.
        """
        self.gamesSoFar += 1

    def endTraining(self):
        # Take off the training wheels
        self.epsilon = 0.0    # no exploration
        self.alpha = 0.0      # no learning
        self.episodesSoFar = 0
        self.gamesSoFar = 0

class RandomAgent(RLAgent):
    def getAction(self, state, actions):
        action = random.choice(actions)
        return action

class QLearningAgent(RLAgent):
    def __init__(self, **args):
        RLAgent.__init__(self, **args)
        self.setValues()

    def setValues(self):
        if self.values:
            self.q_values = util.Counter(self.values)
        else:
            self.q_values = util.Counter()

    def getQValue(self, state, action):
        return self.q_values[state, action]

    def computeValueFromQValues(self, state, legalActions):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        if len(legalActions) == 0:
            return 0.0
        maxVal = -999
        for action in legalActions:
            maxVal = max(maxVal, self.getQValue(state, action))
        return maxVal

    def computeActionFromQValues(self, state, legalActions):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        a = None
        maxVal = -999
        for action in legalActions:
            val = self.getQValue(state, action)
            if val > maxVal:
                maxVal = val
                a = action
        return a

    def getAction(self, state, legalActions):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        action = None
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            action = self.getPolicy(state, legalActions)
        return action

    def update(self, state, action, nextState, reward, legalActions):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        sample = reward + self.discount * self.computeValueFromQValues(nextState, legalActions)
        self.q_values[state, action] += self.alpha * (sample - self.q_values[state, action])

    def getPolicy(self, state, legalActions):
        return self.computeActionFromQValues(state, legalActions)

    def getValue(self, state, legalActions):
        return self.computeValueFromQValues(state, legalActions)

    def stateExtractor(self, board, currentPiece, nextPiece):
        topLine = board.getTopLine()
        return (topLine, currentPiece.shape, nextPiece.shape)

class ApproximateQAgent(QLearningAgent):
    def __init__(self, **args):
        self.featExtractor = Extractor()
        QLearningAgent.__init__(self, **args)

    def setValues(self):
        if self.values:
            self.weights = util.Counter(self.values)
        else:
            self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        return self.getWeights() * self.featExtractor.getFeatures(state, action)

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        features = self.featExtractor.getFeatures(state, action)
        difference = self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState) - self.getQValue(state, action))
        for i in features:
            self.weights[i] += difference * features[i]
