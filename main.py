#!/usr/bin/python3
import structures

exampleGraph = structures.Graph()

#Create the layers and nodes
layerCount = 3
nodeCount = 2
for i in range(0, layerCount):
  layerId = exampleGraph.addLayer()
  layerObj = exampleGraph.getLayer(layerId)
  for i in range(0, nodeCount):
    layerObj.addNode()

#Create the connections
for layerId in range(0, layerCount):
  layer = exampleGraph.getLayer(layerId)
  for nodeId in layer.getNodeList():
    node = layer.getNode(nodeId)
    for i in range(0, nodeCount):
      node.addConnection(i, 16)

print(f"Layers: {exampleGraph.getLayerList()}")
for layer in exampleGraph:
  print(f"Layer: {layer}")
  for node in layer:
    print(f" - Node: {node}")
    for connectionId in node.getConnections():
      print(f"   - Current Node -> {connectionId}: {node.getConnection(connectionId)}")

print(f"\n{exampleGraph}")
