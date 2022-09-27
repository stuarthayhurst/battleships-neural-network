#!/usr/bin/python3
import structures

exampleGraph = structures.Graph()

nodeOne = exampleGraph.addNode()
nodeTwo = exampleGraph.addNode()
nodeThree = exampleGraph.addNode()
nodeFour = exampleGraph.addNode()

exampleGraph.addEdge(nodeOne, nodeTwo, 12)
exampleGraph.addEdge(nodeOne, nodeThree, 6)
exampleGraph.addEdge(nodeTwo, nodeFour, 2)

print(f"Nodes: {exampleGraph.getNodeList()}")
print(exampleGraph.getNode(nodeOne).getConnection(nodeThree))

for node in exampleGraph:
  print(f"{node}")

print(exampleGraph)
