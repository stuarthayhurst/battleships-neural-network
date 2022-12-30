#!/usr/bin/python3

import opponent

shipLengths = [3, 3, 3, 3, 3]
opponent = opponent.Opponent()
opponent.generateGrid(shipLengths)

for row in opponent.grid:
  print(row)
