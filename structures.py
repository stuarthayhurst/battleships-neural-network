#!/usr/bin/python3

"""
 - Define structures used by the model
"""

class Node:
  def __init__(self, name):
    self.name = name
    self.connectedNodesDict = {}

  def addConnection(self, target, weight):
    self.connectedNodesDict[target] = weight

  def getConnection(self, target):
    return self.connectedNodesDict[target]

  def getConnections(self):
    return list(self.connectedNodesDict.keys())

  def __str__(self):
    return str(f"{self.name}: {[weight for weight in self.connectedNodesDict]}")

class Layer:
  def __init__(self, targetNodeCount):
    self.nodeDict = {}
    self.nodeCount = 0

    for i in range(0, targetNodeCount):
      self.addNode()

  def addNode(self, name = None):
    #If name isn't specified, choose a free number
    if name == None:
      name = self.nodeCount
      while name in self.nodeDict.keys():
        name += 1

    #Return if the node already exists
    if name in self.nodeDict.keys():
      return None

    #Add a new node to the dicttionary
    self.nodeDict[name] = Node(name)
    self.nodeCount += 1

    #Return the node's name
    return name

  def getNode(self, name):
    if name in self.nodeDict.keys():
      return self.nodeDict[name]
    return None

  def getNodeList(self):
    return list(self.nodeDict.keys())

  def __iter__(self):
    return iter(self.nodeDict.values())

class Graph:
  def __init__(self, hiddenLayers, nodeCount):
    self.layerDict = {}
    self.layerCount = 0

    for i in range(0, hiddenLayers):
      self.addLayer(nodeCount)

    #Create the connections
    for layerId in range(0, hiddenLayers - 1):
      layer = self.getLayer(layerId)
      for nodeId in layer.getNodeList():
        node = layer.getNode(nodeId)
        for i in range(0, nodeCount):
          node.addConnection(i, 16)

  def addLayer(self, nodeCount, name = None):
    #If name isn't specified, choose a free number
    if name == None:
      name = self.layerCount
      while name in self.layerDict.keys():
        name += 1

    #Return if the node already exists
    if name in self.layerDict.keys():
      return None

    #Add a new node to the dicttionary
    self.layerDict[name] = Layer(nodeCount)
    self.layerCount += 1

    #Return the node's name
    return name

  def getLayer(self, i):
    if i in self.layerDict.keys():
      return self.layerDict[i]
    return None

  def getLayerList(self):
    return list(self.layerDict.keys())

  def __iter__(self):
    return iter(self.layerDict.values())

  def __contains__(self, name):
    return name in self.layerDict.keys()

class Network():
  def __init__(self, hiddenLayers, nodeCount, interfaceWidth, interfaceHeight):
    self.hiddenLayerCount = hiddenLayers
    self.nodesPerLayer = nodeCount
    self.interfaceSize = interfaceHeight * interfaceWidth

    #Create hidden layers as a graph
    self.graph = Graph(self.hiddenLayerCount, self.nodesPerLayer)

    #Create input and output layers
    self.inputLayer = Layer(self.interfaceSize)
    self.outputLayer = Layer(self.interfaceSize)

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
    print(f"Input layer: {self.inputLayer}")
    for node in self.inputLayer:
      print(f" - Node: {node}")
      for connectionId in node.getConnections():
        print(f"   - Current Node -> {connectionId}: {node.getConnection(connectionId)}")

    print(f"Layers: {self.graph.getLayerList()}")
    for layer in self.graph:
      print(f"Layer: {layer}")
      for node in layer:
        print(f" - Node: {node}")
        for connectionId in node.getConnections():
          print(f"   - Current Node -> {connectionId}: {node.getConnection(connectionId)}")

    print(f"Output layer: {self.outputLayer}")
    for node in self.outputLayer:
      print(f" - Node: {node}")
      for connectionId in node.getConnections():
        print(f"   - Current Node -> {connectionId}: {node.getConnection(connectionId)}")

  def runData(self, inputData):
    pass
