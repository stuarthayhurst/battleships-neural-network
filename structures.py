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
