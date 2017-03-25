# mira.py
# -------
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


# Mira implementation
import util
import math
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def calculate(self, validationData,validationLabels):
        correctness1 = 0
        correctness = 0
        guesses = self.classify(validationData)
        for i,j in enumerate(guesses):
            correctness += (validationLabels[i] == j and 1.0 or 0.0)
            acc = (correctness/len(guesses))
        return acc


    def compute_tau(self, W1, w2, y, c):
        tau = min (c, (((W1-w2)*y + 1.0)/ (2.0 *(math.sqrt(y*y)))))
        return tau 

    def changey(self, y, tau):
        y.divideAll(1.0/tau)
        return y
          

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        weights = util.Counter()
        bestAccuracy = None
        score = util.Counter()
        for c in Cgrid:
            weights = self.weights
            for i in range(self.max_iterations):
                for t,y in enumerate(trainingData):
                    #print self.legalLabels
                    for l1 in self.legalLabels:
                        
                        #print "weight[c][l]", weights[l1]
                        #print "print trainingData[t]",trainingData[t]
                        #print "print trainingDLabels[t]",trainingLabels[t]
                        score[l1] = y*weights[l1]
                    maxScore = score.argMax()
                    if not (maxScore == trainingLabels[t]):     
                        Wp = weights[maxScore]
                        w = weights[trainingLabels[t]]
                        
                        tau = min(c, ((Wp-w)*y+1.0)/((y*y)*2))
                        for f in self.features:
                            weights[trainingLabels[t]][f] += tau*y[f]
                            weights[maxScore][f] -= tau*y[f]

                if self.calculate(validationData, validationLabels) > bestAccuracy or bestAccuracy is None:
                    bestAccuracy = self.calculate(validationData, validationLabels)
                    bestWeights = weights

        self.weights = bestWeights

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


