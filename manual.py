#!/usr/bin/python3
import sys
import opponent

#Create opponent
player = opponent.Opponent()
difficulty = sys.argv[1]
player.loadWeights(f"weights/weights-{difficulty}.dmp")

#Print generated grid
print("\nRandom grid:")
player.generateGrid([5, 4, 3, 3, 2])
i = 0
print("   [A, B, C, D, E, F, G]")
for row in player.grid:
  i += 1
  print(f"{i}: {row}")
print()

while True:
  #Make a guess and convert to grid reference
  location = player.makeMove()
  print(f"Guess: {chr(location[0] + 65)}, {location[1] + 1}")

  #Feedback the result to the network
  sending = True
  result = ""
  while sending:
    result = str(input("Result: "))
    if result == "0":
      result = "miss"
      sending = False
    elif result == "1":
      result = "hit"
      sending = False
    else:
      print("Invalid")
  player.feedbackMove(result)
