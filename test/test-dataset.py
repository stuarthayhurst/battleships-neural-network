#!/usr/bin/python3

import neural_network_playground.dataset as dataset

lengths = [0, 1, 10, 100, 1000]

for length in lengths:
  generatedData = dataset.buildDataset(length, 7, 10)
  print(f"{len(generatedData)=}")

print()

size = 10000
hitLimit = 20
testSet = dataset.buildDataset(size, 7, hitLimit)
for pair in testSet:
  hitCount = 0
  for i in testSet[0]:
    if i != 0:
      hitCount += 1
  if hitCount > hitLimit:
    print("FAILED")
    exit(1)

testSet = dataset.buildDataset(1, 7, 0)
board = testSet[0][1]
for i in range(7):
  row = ""
  for j in range(7):
    row += str(board[(i * 7) + j])
  print(row)
