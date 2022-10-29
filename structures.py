#!/usr/bin/python3

"""
 - Define structures used by the model
"""

class Graph:
  def __init__(self, layerCount, nodesPerLayer, connectionsPerNode):
    #Create a set of connections for each nodes for each layer
    # - [layer][target node][source node]
    self.weights = [[[0 for i in range(nodesPerLayer)] for j in range(connectionsPerNode)] for k in range(layerCount)]
    self.biases = [0 for i in range(layerCount)]
