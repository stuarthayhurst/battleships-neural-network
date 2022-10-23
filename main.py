#!/usr/bin/python3
import random, time
import model
import dataset

def getSeconds():
  return time.time_ns() / 1000000000

startTime = getSeconds()

hiddenLayerCount = 3
nodeCount = 10
inputDimensions = 7

networkSize = (((inputDimensions ** 2) * nodeCount) * 2) + (nodeCount ** 2) * (hiddenLayerCount - 1)
weights = [random.randint(0, 10) for i in range(0, networkSize)]

exampleNetwork = model.Network(hiddenLayerCount, nodeCount, 1, inputDimensions ** 2)
exampleNetwork.loadWeights(weights)

print(f"Loaded network in {round(getSeconds() - startTime, 4)}s")
startTime = getSeconds()

datasetSize = 10
boardDimensions = 7
maxHits = (boardDimensions ** 2) - boardDimensions

generatedData = dataset.buildDataset(datasetSize, boardDimensions, maxHits)

print(f"Generated dataset in {round(getSeconds() - startTime, 4)}s")


"""
for gridCount in range(datasetSize):
  for row in generatedData[gridCount][1]:
    print(row)
  print()
  for row in generatedData[gridCount][0]:
    print(row)
  print("\n------------------\n")
"""

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
"""
