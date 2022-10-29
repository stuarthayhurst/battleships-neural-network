#!/usr/bin/python3
import time, random
import model
import dataset

def getSeconds():
  return time.time_ns() / 1000000000

def getWeights(weightFile, networkSize):
  #Attempt to load existing weights from file
  weightsValid = False
  weights = []
  try:
    with open(weightFile) as file:
      weights = file.readlines()

    for i in range(len(weights)):
      weights[i] = float(weights[i].strip("\n"))

    weightsValid = (len(weights) == networkSize)
  except:
    print(f"Couldn't open {weightFile}")

  #Load empty weights if file couldn't be used
  if not weightsValid:
    print("Failed to load existing model, using new empty weights")
    weights = [random.randint(-10, 10) for i in range(networkSize)]
  else:
    print("Loaded existing model")

  return weights

startTime = getSeconds()

#Define network parameters
inputDimensions = 7
networkSize = (inputDimensions ** 2) ** 2

#Load weights in from file, or generate default
weightFile = "weights.dmp"
weights = getWeights(weightFile, networkSize)

#Create model and load weights
exampleNetwork = model.Network(inputDimensions ** 2)
exampleNetwork.loadWeights(weights)

print(f"\nLoaded network in {round(getSeconds() - startTime, 4)}s")
startTime = getSeconds()

#Define dataset parameters and generate data
datasetSize, boardDimensions = 1000, 7
maxHits = (boardDimensions ** 2) - boardDimensions
generatedData = dataset.buildDataset(datasetSize, boardDimensions, maxHits)

print(f"Generated dataset in {round(getSeconds() - startTime, 4)}s")
startTime = getSeconds()

if not exampleNetwork.loadDataset(generatedData):
  print("Failed to load dataset")
  exit(1)

print(f"Loaded dataset in {round(getSeconds() - startTime, 4)}s")
startTime = getSeconds()

iterations, learningRate = 10000, 0.0001
exampleNetwork.trainNetwork(iterations, learningRate)
print(f"Trained network in {round(getSeconds() - startTime, 4)}s")

#Save model weights to file
trainedWeights = exampleNetwork.dumpNetwork()
with open(weightFile, "w") as file:
  for i in range(networkSize):
    file.write(f"{trainedWeights[i]}\n")
