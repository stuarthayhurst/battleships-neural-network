#!/usr/bin/python3

"""
 - Define structures used by the model
"""

class Graph:
  def __init__(self, layerCount, nodesPerLayer, connectionsPerNode):
    #Create a set of connections for each nodes for each layer
    # - [layer][node][connection]
    self.weights = [[[0 for i in range(connectionsPerNode)] for j in range(nodesPerLayer)] for k in range(layerCount)]
