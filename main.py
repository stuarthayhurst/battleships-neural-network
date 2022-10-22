#!/usr/bin/python3
import random
import structures

hiddenLayerCount = 3
nodeCount = 10
inputDimensions = 2

exampleNetwork = structures.Network(hiddenLayerCount, nodeCount, 1, inputDimensions ** 2)

networkSize = (((inputDimensions ** 2) * nodeCount) * 2) + (nodeCount ** 2) * (hiddenLayerCount - 1)
exampleNetwork.dumpNetwork()
print(networkSize)

weights = [random.randint(0, 10) for i in range(0, networkSize)]
exampleNetwork.loadWeights(weights)

exampleNetwork.dumpNetwork()

"""
Todo:
 - Dataset generation / saving (file storage)
   - Generate n boards, and use for e epochs
 - Network pass implementation / sampling
 - Network training / improvement
   - Save activiation threshold / function
   - Optimise weight modification time
   - Add training / loss metrics
 - Network weight saving (file storage)
"""

"""
Notes:
 - Create nodes at same time as weights (Mention as a load time optimisation)
 - Add method to query network size (use to verify whether weights can be loaded)
 - Keep structures and network separate (do differently for implementation)
"""
