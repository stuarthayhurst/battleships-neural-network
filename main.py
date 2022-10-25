#!/usr/bin/python3
import random, time
import model
import dataset

def getSeconds():
  return time.time_ns() / 1000000000

startTime = getSeconds()

#Define network parameters
hiddenLayerCount, nodeCount, inputDimensions = 3, 10, 7
networkSize = (((inputDimensions ** 2) * nodeCount) * 2) + (nodeCount ** 2) * (hiddenLayerCount - 1)

#Attempt to load existing weights from file
loadWeights, weightsValid, weights = True, False, []
weightFile = "weights.dmp"
try:
  if loadWeights:
    with open(weightFile) as file:
      weights = file.readlines()

    for i in range(len(weights)):
      weights[i] = float(weights[i].strip("\n"))

    weightsValid = (len(weights) == networkSize)
except:
  print(f"Couldn't open {weightFile}")

if not weightsValid:
  print("Failed to load existing model, using new empty weights\n")
  weights = [0 for i in range(0, networkSize)]
else:
  print("Loaded existing model\n")

#Create model and load weights
exampleNetwork = model.Network(hiddenLayerCount, nodeCount, 1, inputDimensions ** 2)
exampleNetwork.loadWeights(weights)

print(f"Loaded network in {round(getSeconds() - startTime, 4)}s")
startTime = getSeconds()

#Define dataset parameters and generate data
datasetSize, boardDimensions = 10, 7
maxHits = (boardDimensions ** 2) - boardDimensions
generatedData = dataset.buildDataset(datasetSize, boardDimensions, maxHits)

print(f"Generated dataset in {round(getSeconds() - startTime, 4)}s")
startTime = getSeconds()

print()
print(f"User board: {generatedData[0][0]}")
print(f"Board: {generatedData[0][1]}")
print(exampleNetwork.runData(generatedData[0][0]))
print()

print(f"Ran network in {round(getSeconds() - startTime, 4)}s")

#Save model weights to file
trainedWeights = exampleNetwork.dumpNetwork()
with open(weightFile, "w") as file:
  for i in range(networkSize):
    file.write(f"{trainedWeights[i]}\n")

"""
Todo:
 - Generate n boards, and use for e epochs
 - Process returned results
 - Network training / improvement
   - Potentially add more activation layers
   - Add training / loss metrics
"""
