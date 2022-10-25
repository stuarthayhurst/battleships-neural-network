#!/usr/bin/python3
import structures
import math

class Network():
  def __init__(self, hiddenLayers, nodeCount, interfaceWidth, interfaceHeight):
    self.hiddenLayerCount = hiddenLayers
    self.nodesPerLayer = nodeCount
    self.interfaceSize = interfaceHeight * interfaceWidth

    #Create empty dataset
    self.dataset = []

    #Create hidden layers as a graph
    self.graph = structures.Graph(self.hiddenLayerCount, self.nodesPerLayer)

    #Create input and output layers
    self.inputLayer = structures.Layer(self.interfaceSize)
    self.outputLayer = structures.Layer(self.interfaceSize)

    #Setup input layer weights
    inputNodeList = self.inputLayer.getNodeList() 
    for i in range(0, self.interfaceSize):
      currentNode = self.inputLayer.getNode(inputNodeList[i])
      for j in range(0, self.nodesPerLayer):
        currentNode.addConnection(j, 16)

    #Setup output layer weights
    outputNodeList = self.outputLayer.getNodeList()
    finalLayer = self.graph.getLayer(self.hiddenLayerCount - 1)
    finalLayerNodes = finalLayer.getNodeList()
    for i in range(0, self.nodesPerLayer):
      currentNode = finalLayer.getNode(finalLayerNodes[i])
      for j in range(0, self.interfaceSize):
        currentNode.addConnection(j, 16)

  def loadWeights(self, weights):
    weightIndex = 0

    #Load weights for input layer
    for i in range(0, self.interfaceSize):
      currentNode = self.inputLayer.getNode(i)
      for j in range(0, self.nodesPerLayer):
        currentNode.addConnection(j, weights[weightIndex])
        weightIndex += 1

    #Load weights for hidden layers
    for l in range(0, self.hiddenLayerCount - 1):
      currentLayer = self.graph.getLayer(l)
      for n in range(0, self.nodesPerLayer):
        currentNode = currentLayer.getNode(n)
        for t in range(0, self.nodesPerLayer):
          currentNode.addConnection(t, weights[weightIndex])
          weightIndex += 1

    #Load weights for output layer
    finalLayer = self.graph.getLayer(self.hiddenLayerCount - 1)
    for i in range(0, self.nodesPerLayer):
      currentNode = finalLayer.getNode(i)
      for j in range(0, self.interfaceSize):
        currentNode.addConnection(j, weights[weightIndex])
        weightIndex += 1

  def dumpNetwork(self):
    weights = []

    for node in self.inputLayer:
      for connectionId in node.getConnections():
        weights.append(node.getConnection(connectionId))

    for layer in self.graph:
      for node in layer:
        for connectionId in node.getConnections():
          weights.append(node.getConnection(connectionId))

    for node in self.outputLayer:
      for connectionId in node.getConnections():
        weights.append(node.getConnection(connectionId))

    return weights

  def sampleData(self, inputData):
    if len(inputData) != self.interfaceSize:
      print("Input data must match interface size")
      return False

    workingValues = [0 for i in range(self.nodesPerLayer)]

    #Apply weights on input layer
    for inputCount in range(self.interfaceSize):
      dataPoint = inputData[inputCount]
      inputNode = self.inputLayer.getNode(inputCount)
      for i in range(self.nodesPerLayer):
        weight = inputNode.getConnection(i)
        workingValues[i] += dataPoint * weight

    #Apply activation function
    for i in range(self.nodesPerLayer):
      workingValues[i] = 1 / (1 + (math.e ** workingValues[i]))

    #Apply weights on hidden layers
    for layerCount in range(self.hiddenLayerCount - 1):
      #Copy working values to input, and reset working
      inputValues = [i for i in workingValues]
      workingValues = [0 for i in range(self.nodesPerLayer)]

      #Iterate over every node in the layer
      currentLayer = self.graph.getLayer(layerCount)
      for nodeCount in range(self.nodesPerLayer):
        #Apply the weights to the input values
        currentNode = currentLayer.getNode(nodeCount)
        for i in range(self.nodesPerLayer):
          weight = currentNode.getConnection(i)
          workingValues[i] += inputValues[nodeCount] * weight

      #Apply activation function to each neuron (once per layer)
      for i in range(self.nodesPerLayer):
        workingValues[i] = 1 / (1 + (math.e ** workingValues[i]))

    #Apply weights on output layer
    finalLayer = self.graph.getLayer(self.hiddenLayerCount - 1)
    inputValues = [i for i in workingValues]
    workingValues = [0 for i in range(self.interfaceSize)]
    for inputCount in range(self.nodesPerLayer):
      currentNode = finalLayer.getNode(inputCount)
      for i in range(self.interfaceSize):
        weight = currentNode.getConnection(i)
        workingValues[i] += inputValues[nodeCount] * weight

    #Apply activation function to final layer
    for i in range(self.interfaceSize):
      workingValues[i] = 1 / (1 + (math.e ** workingValues[i]))

    return workingValues

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
      for j in [0, 1] :
        self.dataset[i][j] = dataset[i][j]

    return True

  def trainData(self):
    pass
