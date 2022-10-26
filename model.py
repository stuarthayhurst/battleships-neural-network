#!/usr/bin/python3
import structures
import math

import random

class Network():
  def __init__(self, hiddenLayerCount, nodesPerLayer, inputSize):
    self.hiddenLayerCount = hiddenLayerCount
    self.hiddenLayerStructLength = hiddenLayerCount - 1
    self.nodesPerLayer = nodesPerLayer
    self.interfaceSize = inputSize

    #Create empty dataset
    self.dataset = []

    #Create input, hidden and output layers as a graphs
    self.hiddenLayers = structures.Graph(self.hiddenLayerCount - 1, self.nodesPerLayer, self.nodesPerLayer)
    self.inputLayer = structures.Graph(1, self.interfaceSize, self.nodesPerLayer)
    self.outputLayer = structures.Graph(1, self.nodesPerLayer, self.interfaceSize)

  def loadWeights(self, weights):
    weightIndex = 0

    #Load weights for input layer
    for nodeCount in range(self.interfaceSize):
      for targetNode in range(self.nodesPerLayer):
        self.inputLayer.weights[0][nodeCount][targetNode] = weights[weightIndex]
        weightIndex += 1

    #Load weights for hidden layers
    for layerCount in range(self.hiddenLayerStructLength):
      for nodeCount in range(self.nodesPerLayer):
        for targetNode in range(self.nodesPerLayer):
          self.hiddenLayers.weights[layerCount][nodeCount][targetNode] = weights[weightIndex]
          weightIndex += 1

    #Load weights for output layer
    for nodeCount in range(self.nodesPerLayer):
      for targetNode in range(self.interfaceSize):
        self.outputLayer.weights[0][nodeCount][targetNode] = weights[weightIndex]
        weightIndex += 1

  def dumpNetwork(self):
    weights = []

    for node in self.inputLayer.weights[0]:
      for targetNode in node:
        weights.append(targetNode)

    for layer in self.hiddenLayers.weights:
      for node in layer:
        for targetNode in node:
          weights.append(targetNode)

    for node in self.outputLayer.weights[0]:
      for targetNode in node:
        weights.append(targetNode)

    return weights

  def sigmoidActivation(self, result):
    return 1 / (1 + (math.e ** result))

  def sampleData(self, inputData, returnWorkings = False):
    if len(inputData) != self.interfaceSize:
      print("Input data must match interface size")
      return False

    workingValuesList = [[] for i in range(self.hiddenLayerCount + 1)]

    workingValuesList[0] = [0 for i in range(self.nodesPerLayer)]

    #Apply weights on input layer
    for inputCount in range(self.interfaceSize):
      dataPoint = inputData[inputCount]
      inputNode = self.inputLayer.getNode(inputCount)
      for i in range(self.nodesPerLayer):
        weight = inputNode.getConnection(i)
        workingValuesList[0][i] += dataPoint * weight

    #Apply activation function
    for i in range(self.nodesPerLayer):
      workingValuesList[0][i] = self.activation(workingValuesList[0][i])

    #Apply weights on hidden layers
    for layerCount in range(self.hiddenLayerCount - 1):
      #Copy working values to input, and reset working
      inputValues = [i for i in workingValuesList[layerCount]]
      workingValuesList[layerCount + 1] = [0 for i in range(self.nodesPerLayer)]

      #Iterate over every node in the layer
      currentLayer = self.graph.getLayer(layerCount)
      for nodeCount in range(self.nodesPerLayer):
        #Apply the weights to the input values
        currentNode = currentLayer.getNode(nodeCount)
        for i in range(self.nodesPerLayer):
          weight = currentNode.getConnection(i)
          workingValuesList[layerCount + 1][i] += inputValues[nodeCount] * weight

      #Apply activation function to each neuron (once per layer)
      for i in range(self.nodesPerLayer):
        workingValuesList[layerCount + 1][i] = self.activation(workingValuesList[layerCount + 1][i])

    #Apply weights on output layer
    finalLayer = self.graph.getLayer(self.hiddenLayerCount - 1)
    inputValues = [i for i in workingValuesList[self.hiddenLayerCount - 1]]
    workingValuesList[self.hiddenLayerCount] = [0 for i in range(self.interfaceSize)]
    for inputCount in range(self.nodesPerLayer):
      currentNode = finalLayer.getNode(inputCount)
      for i in range(self.interfaceSize):
        weight = currentNode.getConnection(i)
        workingValuesList[self.hiddenLayerCount][i] += inputValues[nodeCount] * weight

    #Apply activation function to final layer
    for i in range(self.interfaceSize):
      workingValuesList[self.hiddenLayerCount][i] = self.activation(workingValuesList[self.hiddenLayerCount][i])

    if returnWorkings:
      return workingValuesList
    else:
      return workingValuesList[self.hiddenLayerCount]

  def loadDataset(self, dataset):
    for pair in dataset:
      if len(pair) != 2:
        print("Data must be paired")
        return False

      if pair[0] == None or pair[1] == None:
        print("Data points can't be empty")
        return False

    #Copy passed dataset into structure
    for i in range(len(dataset)):
      self.dataset.append([None, None])
      for j in [0, 1]:
        self.dataset[i][j] = dataset[i][j]

    return True

  def trainDataPair(self, dataPair, verbose = False):
    #Run the data through the network
    workingValues = self.sampleData(dataPair[0], True)
    results = workingValues[len(workingValues) - 1]

    #Calculate the MSE of the prediction
    outputLength = len(dataPair[0])
    meanErrors = [0 for i in range(outputLength)]
    totalError = 0
    for i in range(outputLength):
      meanErrors[i] = (results[i] - dataPair[1][i]) ** 2
      totalError += meanErrors[i]
    totalError /= outputLength

    if verbose:
      print(f"Input    : {dataPair[0]}")
      print(f"Expected : {dataPair[1]}")
      print(f"Result   : {results}")
      print(f"Error    : {meanErrors}")
      print(f"Total    : {totalError}")

    #
    #Adjust the weight of each connection to a neuron by +/- the error

#Make this decided by user
    learningRate = 0.1

    def sigD(x):
      return (1 / (1 + (math.e ** -x))) * (1 - (1 / (1 + (math.e ** -x))))

    for i in range(len(results)):
      result = results[i]
      error = meanErrors[i]

      dpredic = 2 * (result - dataPair[1][i])
      dlayer = sigD(result)

      correctionFactor = dpredic * dlayer

    #Iterate over final layer weights
      finalLayer = self.graph.getLayer(self.hiddenLayerCount - 1)
      for j in range(self.nodesPerLayer):
        currentNode = finalLayer.getNode(j)
        weight = currentNode.getConnection(i)

        #weightCorrection = (weight * correctionFactor * learningRate)
        weightCorrection = (result - dataPair[1][i]) * learningRate
        #weightCorrection = error * result * learningRate
        #print(weightCorrection)

        currentNode.addConnection(i, (weight - weightCorrection))

#Unify this and prev

    for layerCount in range(self.hiddenLayerCount - 1, 0, -1):
      currentLayer = self.graph.getLayer(layerCount - 1)
      workingValuesIndex = len(workingValues) - (self.hiddenLayerCount - layerCount) - 1
      currentWorkingValues = workingValues[workingValuesIndex]
      #print(workingValuesIndex)
      #print(len(workingValues) - 1)
      #input()
      for nodeCount in range(self.nodesPerLayer):
        currentNode = currentLayer.getNode(nodeCount)
        for targetNode in range(self.nodesPerLayer):
          weight = currentNode.getConnection(targetNode)

          #Calculate correction
          weightC = sigD(currentWorkingValues[targetNode])

          currentNode.addConnection(targetNode, weight - weightC)


  def trainNetwork(self, iterations):
    dataCount = len(self.dataset)
    for i in range(iterations):
      dataPair = self.dataset[i % dataCount]
      verbose = False
      if (i % 1 == 0):
        verbose = True
      self.trainDataPair(dataPair, verbose)
