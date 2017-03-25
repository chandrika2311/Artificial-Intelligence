# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        new_Value = self.values
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        
        #print "iterations:",self.iterations
        #print"self.discount = discount", self.discount
        #print "self.values = util.Counter()", self.values
        
        #list_of_states = self.mdp.getStates()
        #Do 100 times: i.e iterations times
        #loop over all the states in mdp.getStates()
        for i in range(self.iterations):
        	new_Value = util.Counter()
        	for state in self.mdp.getStates():
        		if self.mdp.isTerminal(state):
        			new_Value[state] = 0
        		else:

        			maximum_q_value = float("-inf")
        			possible_actions = self.mdp.getPossibleActions(state)
        			#print "possible_actions:", possible_actions
        			for action in possible_actions:
        				#print"action:", action
        				qvalue = self.computeQValueFromValues(state,action)
        				maximum_q_value = max(qvalue,maximum_q_value)
        				new_Value[state] = maximum_q_value

        	self.values = new_Value
        	

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #take an action and state and calculate the Q value for them here:
        
        qval = 0
        for transition in self.mdp.getTransitionStatesAndProbs(state, action):
        	nextState = transition[0]
        	probability = transition[1]
        	reward = self.mdp.getReward(state, action, transition[0])
        	
        	qval += probability * (self.mdp.getReward(state, action, nextState) + (self.discount * self.values[nextState]))
        	

        return qval
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        
        possible_actions = self.mdp.getPossibleActions(state)
        
        if len(possible_actions) == 0:
        	return None
        maxaction = None
        maximum_q_value = float("-inf")	
        for action in possible_actions:
        	qvalue = self.computeQValueFromValues(state,action)
        	if qvalue > maximum_q_value:
        		a = action
        		maximum_q_value = qvalue
        		
        return a	
        #util.raiseNotDefined()

    def getPolicy(self, state):
    	
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
