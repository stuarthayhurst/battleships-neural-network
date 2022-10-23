#!/usr/bin/python3
import structures

class Network():
  def __init__(self, hiddenLayers, nodeCount, interfaceWidth, interfaceHeight):
    self.hiddenLayerCount = hiddenLayers
    self.nodesPerLayer = nodeCount
    self.interfaceSize = interfaceHeight * interfaceWidth

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
