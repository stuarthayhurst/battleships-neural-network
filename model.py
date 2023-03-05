#!/usr/bin/python3
import numpy, random

#Class to represent a specialised graph, for neural network weights
class Graph:
  def __init__(self, layerCount, nodesPerLayer, connectionsPerNode):
    #Create a set of connections for each nodes for each layer
    # - [layer][target node][source node]
    self.weights = [[[0 for i in range(nodesPerLayer)] for j in range(connectionsPerNode)] for k in range(layerCount)]

#Class to contain the neural network
class Network:
  def __init__(self, inputSize):
    self.interfaceSize = inputSize

    #Create empty dataset
    self.dataset = []

    #Create input layer weights
    self.weightGraph = Graph(1, self.interfaceSize, self.interfaceSize)

  #Load a list of floats as the network's weights
  def loadWeights(self, weights):
    weightIndex = 0

    #Load weights for input layer
    for targetNode in range(self.interfaceSize):
      for nodeCount in range(self.interfaceSize):
        self.weightGraph.weights[0][targetNode][nodeCount] = weights[weightIndex]
        weightIndex += 1

  #Output a list of floats for the network's current weights
  def dumpNetwork(self):
    weights = []

    for targetNode in self.weightGraph.weights[0]:
      for node in targetNode:
        weights.append(node)

    return weights

  #Sigmoid activation function, called on each output
  # - Shifts any numerical input into the range 0 - 1
  def sigmoidActivation(self, result):
    return 1 / (1 + numpy.exp(-result))

  #Generate probabilities from input data
  def sampleData(self, inputData, returnWorkings = False):
    #Check the size of the data
    if len(inputData) != self.interfaceSize:
      print("Input data must match interface size")
      return False

    preActivationValues = []

    #Apply input layer weights
    workingValues = []
    workingValues.append([])
    preActivationValues.append([])
    for targetNode in self.weightGraph.weights[0]:
      workingValues[0].append(numpy.dot(inputData, targetNode))

    #Apply activation function to input layer
    for i in range(self.interfaceSize):
      preActivationValues[0].append(workingValues[0][i])
      workingValues[0][i] = self.sigmoidActivation(workingValues[0][i])

    #Either return all values, or only final values
    # - Useful when training the network
    if returnWorkings:
      return workingValues, preActivationValues
    else:
      return workingValues[len(workingValues) - 1]

  #Take a list of pairs of boards, load into the network for training
  def loadDataset(self, dataset):
    #Validate pairs
    for pair in dataset:
      if len(pair) != 2:
        print("Data must be paired")
        return False

      #Validate data exists
      if pair[0] == None or pair[1] == None:
        print("Data points can't be empty")
        return False

    #Copy the dataset into instance
    self.dataset = dataset

    return True

  #Derivative of sigmoid function, used to train with gradient descent
  def sigmoidDerivative(self, variable):
    return self.sigmoidActivation(variable) * (1 - self.sigmoidActivation(variable))

  #Train the network on a specific data pair (input + solution)
  def trainDataPair(self, dataPair, learningRate, verbose):
    #Run the data through the network
    workingValues, preActivationValues = self.sampleData(dataPair[0], True)
    results = workingValues[len(workingValues) - 1]

    #Verbose toggle, as constant buffer flushing hurts performance
    if verbose:
      #Calculate the MSE of the prediction
      outputLength = len(dataPair[0])
      averageCost = 0
      meanCosts = []
      for i in range(outputLength):
        meanCosts.append((results[i] - dataPair[1][i]) ** 2)
        averageCost += meanCosts[i]
      averageCost /= outputLength
      print(f"Input    : {dataPair[0]}\n")
      print(f"Expected : {[round(float(i), 2) for i in dataPair[1]]}\n")
      print(f"Result   : {[round(float(i), 2) for i in results]}\n")
      print(f"Error    : {meanCosts}\n")
      print(f"Total    : {averageCost}\n")

    #Create temporary weight store
    tempWeights = []
    for targetNode in range(self.interfaceSize):
      tempWeights.append([])
      for previousNode in range(self.interfaceSize):
        tempWeights[targetNode].append(0)

    #Calculate the change required to improve the network
    for targetNode in range(self.interfaceSize):
      result = results[targetNode]
      offset = result - dataPair[1][targetNode]
      dEP = 2 * (offset)
      dPL = self.sigmoidDerivative(preActivationValues[0][targetNode])
      for previousNode in range(self.interfaceSize):
        dLW = dataPair[0][previousNode]
        dEL = dEP * dPL * dLW
        tempWeights[targetNode][previousNode] += dEL * learningRate

      return tempWeights

  #Wrapper function to train the network for a given number of batches
  def trainNetwork(self, batchCount, batchSize, learningRate):
    dataCount = len(self.dataset)
    for i in range(batchCount):
      verbose = False
      #Output every 500 pairs, as to not reduce performance
      if ((i * batchSize) % 500 < batchSize):
        verbose = True

      #Accumulate the changes for all samples in a batch
      weightChanges = []
      for x in range(batchSize):
        dataPair = self.dataset[random.randint(0, dataCount - 1)]
        weightChanges.append(self.trainDataPair(dataPair, learningRate, verbose))
        if verbose:
          verbose = False

      #Average collected samples
      avg = [[0 for k in range(self.interfaceSize)] for l in range(self.interfaceSize)]
      for weightCount in range(batchSize):
        for targetNode in range(self.interfaceSize):
          for previousNode in range(self.interfaceSize):
            avg[targetNode][previousNode] += weightChanges[weightCount][targetNode][previousNode]

      #Apply the changes to the weights
      for targetNode in range(self.interfaceSize):
        for previousNode in range(self.interfaceSize):
          self.weightGraph.weights[0][targetNode][previousNode] -= avg[targetNode][previousNode] / batchSize

      #Print batch number every 500 pairs
      if ((i * batchSize) % 500 < batchSize):
        print(f"Batch {i} / {batchCount} ({round((i / batchCount) * 100, 2)}%)")
