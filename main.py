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

print(generatedData[0][0])
print(generatedData[0][1])

#Maybe represent inputs as a vector
#Include x coord, y coord, has been guessed, has been hit
#3 dimensional vector (x, y, state)
#Whole datapiece as a vector?
#Output is correct is it's a vector with a 1 over an unhit ship

#Match number of nodes and input size
#Use regular division / multiplication with weights
#Activation function on final layer
#Average / handle cumulative data passing through
#Tweak how weights are modified (error calculated)
#Tweak state representation

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
