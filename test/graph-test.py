#!/usr/bin/python3

class Graph:
  def __init__(self, layerCount, nodesPerLayer, connectionsPerNode):
    #Create a set of connections for each nodes for each layer
    # - [layer][target node][source node]
    self.weights = [[[0 for i in range(nodesPerLayer)] for j in range(connectionsPerNode)] for k in range(layerCount)]

graph = Graph(3, 4, 4)

i = 0
for layer in graph.weights:
  i += 1
  print(f"{i}: {layer}")
