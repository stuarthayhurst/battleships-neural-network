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

class Graph:
  def __init__(self):
    self.nodesDict = {}
    self.nodeCount = 0

  def getNode(self, name):
    if name in self.nodesDict.keys():
      return self.nodesDict[name]
    return None
 
  def getNodeList(self):
    return list(self.nodesDict.keys())

  def addNode(self, name = None):
    #If name isn't specified, choose a free number
    if name == None:
      name = self.nodeCount
      while name in self.nodesDict.keys():
        name += 1

    #Return if the node already exists
    if name in self.nodesDict.keys():
      return None

    #Add a new node to the dicttionary
    self.nodesDict[name] = Node(name)
    self.nodeCount += 1

    #Return the node's name
    return name

  def addEdge(self, head, tail, weight = 0, directional = False):
    #Check head node exists
    if head not in self.nodesDict.keys():
      return None

    #Check tail node exists
    if tail not in self.nodesDict.keys():
      return None

    #Create the connections
    self.nodesDict[head].addConnection(tail, weight)
    if not directional:
      self.nodesDict[tail].addConnection(head, weight)

    #Return the connection's weight
    return weight

  def __iter__(self):
    return iter(self.nodesDict.values())

  def __contains__(self, name):
    return name in self.nodesDict.keys()
