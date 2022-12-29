#!/usr/bin/python3

import interface

def isDone(grid):
  for row in grid:
    for col in row:
      if col == 1:
        return False
  return True

#Setup the opponent
opponent = interface.Opponent()
opponent.generateGrid([5, 4, 3, 3, 2])

#Generate full grid
playerGrid = [[1 for i in range(7)] for j in range(7)]

guesses = 0
while not isDone(playerGrid):
  guesses += 1
  guess = opponent.makeMove()
  if playerGrid[guess[1]][guess[0]] == 1:
    opponent.feedbackMove("hit")
    playerGrid[guess[1]][guess[0]] = 0
  else:
    opponent.feedbackMove("miss")

print(f"Took {guesses} attempts")
for row in playerGrid:
  print(row)
