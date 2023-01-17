#!/usr/bin/python3

#Lists for testing
convertedGrid = [0 for i in range (49)]
guesses = [0 for i in range(49)]

#Generate test probabilities
guesses[11] = 0.2
guesses[13] = 0.4
guesses[18] = 1.0
guesses[19] = 0.1

#Mark location 18 as guessed
convertedGrid[18] = 1

maxGuess = 0
maxGuessIndex = -1
for i in range(len(guesses)):
  if guesses[i] >= maxGuess:
    if convertedGrid[i] == 0:
      maxGuess = guesses[i]
      maxGuessIndex = i
guess = maxGuessIndex

#x and y flipped compared to other sections of code
#This is because the neural network returns data in order horizontally, then vertically
#Other sections of code enumerate the grid vertically then horizontally
x = guess % 7
y = guess // 7

print(f"{(x, y)=}")
