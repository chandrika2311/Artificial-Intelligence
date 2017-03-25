# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qval = {}


    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
      
        "*** YOUR CODE HERE ***"
        #find qvalue of a stata (state action)
        #check if the state ,action pair exists in the qvalue list :
        

        if(state,action) not in self.qvalue:
          return 0
        else:
          #return the Q node value otherwise
          return self.qvalue[(state,action)]
        """  
        if (state,action) not in self.qval:#if the state and action pair is not in the self.qval then return 0
          return 0
        else:#else if the state and action pair is  in the self.qval then return the pair value        
          return self.qval[(state, action)]




    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:#if no legal action found from the current state
          return 0# return zero as nothing can be done

        maximum_qvalue = float("-inf")#Initialize the value and result
        max_action = None
        for action in legalActions:#iterating over the legal actions
          current_q_value = self.getQValue(state, action)# the current q values calculated with help of getQValue function.
          #if maximum_qvalue == None:
          if maximum_qvalue == None or current_q_value > maximum_qvalue:# if the maximum value is less than the current value then replace them with each other
            #if maximum_qvalue == None:
            maximum_qvalue = current_q_value
            #  maximum_qvalue = 0
            max_action = action
        return maximum_qvalue
        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
     
        if len(legalActions) == 0:#if no legal action found from the current state
          return 0# return zero as nothing can be done

        maximum_qvalue = float("-inf")#Initialize the value and result
        max_action = None
        for action in legalActions:#iterating over the legal actions
          current_q_value = self.getQValue(state, action)# the current q values calculated with help of getQValue function.
          #if maximum_qvalue == None:
          if maximum_qvalue == None or current_q_value > maximum_qvalue:# if the maximum value is less than the current value then replace them with each other
            #if maximum_qvalue == None:
            maximum_qvalue = current_q_value
            #  maximum_qvalue = 0
            max_action = action
        return max_action
        
        util.raiseNotDefined()

    def getAction(self, state):
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
        "*** YOUR CODE HERE ***"
        Actions = self.getLegalActions(state)
        #meaning it chooses random actions an epsilon fraction of the time
        if len(Actions) == 0:
          return 0
          #when on the flip of coin we chose randomly
        if util.flipCoin(self.epsilon):#when on the flip of coin we chose randomly
          return random.choice(Actions)# take a random choice from the legal actiona
        #compute with this action now instead of the conventional actions
        return self.computeActionFromQValues(state)
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"


        if (state, action) not in self.qval:
          #if the state and action pair is in the self.qval then get the tuple
          self.qval[(state, action)] = 0
          #if the state and action pair is in the self.qval then get the tuple
        curq = self.qval[(state, action)]
        #if the state and action pair is in the self.qval then get the tuple
        
        nextq = self.computeValueFromQValues(nextState)
        #if the state and action pair is in the self.qval then get the tuple
        #if the state and action pair is in the self.qval then get the tuple
        #if the state and action pair is in the self.qval then get the tuple
        sprime = reward + (self.discount * nextq) - curq
        #if the state and action pair is in the self.qval then get the tuple
        self.qval[(state, action)] = curq + (self.alpha * sprime)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        


    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"

        util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
