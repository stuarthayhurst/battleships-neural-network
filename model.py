#!/usr/bin/python3
import structures
import numpy, random

class Network():
  def __init__(self, inputSize):
    self.interfaceSize = inputSize

    #Create empty dataset
    self.dataset = []

    #Create input layer weights
    self.inputLayer = structures.Graph(1, self.interfaceSize, self.interfaceSize)

  def loadWeights(self, weights):
    weightIndex = 0

    #Load weights for input layer
    for targetNode in range(self.interfaceSize):
      for nodeCount in range(self.interfaceSize):
        self.inputLayer.weights[0][targetNode][nodeCount] = weights[weightIndex]
        weightIndex += 1

  def dumpNetwork(self):
    weights = []

    for targetNode in self.inputLayer.weights[0]:
      for node in targetNode:
        weights.append(node)

    return weights

  def sigmoidActivation(self, result):
    return 1 / (1 + numpy.exp(-result))

  def sampleData(self, inputData, returnWorkings = False):
    if len(inputData) != self.interfaceSize:
      print("Input data must match interface size")
      return False

    preActivationValues = []

    #Apply input layer weights
    workingValues = []
    workingValues.append([])
    preActivationValues.append([])
    for targetNode in self.inputLayer.weights[0]:
      result = numpy.dot(inputData, targetNode)
      workingValues[0].append(result + self.inputLayer.biases[0])

    #Apply activation function to input layer
    for i in range(self.interfaceSize):
      preActivationValues[0].append(workingValues[0][i])
      workingValues[0][i] = self.sigmoidActivation(workingValues[0][i])

    if returnWorkings:
      return workingValues, preActivationValues
    else:
      return workingValues[len(workingValues) - 1]

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

  def sigmoidDerivative(self, variable):
    return self.sigmoidActivation(variable) * (1 - self.sigmoidActivation(variable))

  def trainDataPair(self, dataPair, learningRate, verbose):
    #Run the data through the network
    workingValues, preActivationValues = self.sampleData(dataPair[0], True)
    results = workingValues[len(workingValues) - 1]

    #Calculate the MSE of the prediction
    outputLength = len(dataPair[0])
    meanCosts = []
    averageCost = 0
    for i in range(outputLength):
      meanCosts.append((results[i] - dataPair[1][i]) ** 2)
      averageCost += meanCosts[i]
    averageCost /= outputLength

    if verbose:
      print(f"Input    : {dataPair[0]}\n")
      print(f"Expected : {[round(float(i), 2) for i in dataPair[1]]}\n")
      print(f"Result   : {[round(float(i), 2) for i in results]}\n")
      print(f"Error    : {meanCosts}\n")
      print(f"Total    : {averageCost}\n")

    debug = False
    if debug:
      print(f"Finals: {workingValues}")
      print(f"Inputs: {preActivationValues}")

    for targetNode in range(self.interfaceSize):
      result = results[targetNode]
      offset = result - dataPair[1][targetNode]
      dEP = 2 * (offset)
      dPL = self.sigmoidDerivative(preActivationValues[0][targetNode])
      dEB = dEP * dPL
      for previousNode in range(self.interfaceSize):
        dLW = dataPair[0][previousNode]
        dEL = dEP * dPL * dLW
        self.inputLayer.weights[0][targetNode][previousNode] -= dEL * learningRate
        self.inputLayer.biases[0] -= dEB * learningRate

  def trainNetwork(self, iterations, learningRate):
    dataCount = len(self.dataset)
    for i in range(iterations):
      verbose = False
      if (i % 100 == 0):
        verbose = True

      dataPair = self.dataset[random.randint(0, dataCount - 1)]
      self.trainDataPair(dataPair, learningRate, verbose)

      if verbose:
        print(f"{i} / {iterations} ({round((i / iterations) * 100, 2)}%)")
