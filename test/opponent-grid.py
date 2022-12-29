#!/usr/bin/python3

import interface

shipLengths = [3, 3, 3, 3, 3]
opponent = interface.Opponent()
opponent.generateGrid(shipLengths)

for row in opponent.grid:
  print(row)
