#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import csv
import os

import opponent
import screens
import classes

def readStats(statsFile):
  statsPath = "stats.csv"
  statsDict = {
    "totalGames": 0,
    "totalWins": 0,
    "totalMoves": 0,
    "totalHits": 0
  }

  #Read CSV into dictionary, if it exists
  if os.path.isfile(statsPath):
    with open(statsPath) as statsFile:
      reader = csv.reader(statsFile, delimiter = ",")
      for row in reader:
        statsDict[row[0]] = int(row[1])
  else:
    return statsDict, False

  return statsDict, True

#Wrapper class for GTK
class Window(classes.Element):
  def __init__(self, uiFilePath):
    super().__init__(uiFilePath, "main-window")

  def setTitle(self, title):
    self.headerBar.set_title(title)

  def setupWindow(self):
    #Create and set a header bar
    self.headerBar = Gtk.HeaderBar()
    self.headerBar.set_title("Window")
    self.headerBar.set_show_close_button(True)
    self.headerBar.show_all()
    self.element.set_titlebar(self.headerBar)

    #Add icon to button and connect signal
    image = Gtk.Image.new_from_file("assets/statistics.png")
    statsButton = self.builder.get_object("statistics-button")
    statsButton.set_image(image)
    statsButton.connect("clicked", self.statsButtonPressed)

  def statsButtonPressed(self, button):
    #Load stats in from file, and return status
    statsPath = "stats.csv"
    statsDict, foundFile = readStats(statsPath)

    #Calculate statistics and create pop-up message, or handle case of no file
    windowMessage = ""
    if foundFile:
      #Check for perfect track record, to avoid potential division by zero
      winLossRatio = ""
      if statsDict["totalWins"] == statsDict["totalGames"]:
        winLossRatio = "∞"
      else:
        winLossRatio = statsDict["totalWins"] / (statsDict["totalGames"] - statsDict["totalWins"])
        winLossRatio = str(round(winLossRatio, 2))

      #Check for hit rate, to avoid potential division by zero
      hitMissRatio = ""
      if statsDict["totalHits"] == statsDict["totalMoves"]:
        hitMissRatio = "∞"
      else:
        hitMissRatio = statsDict["totalHits"] / (statsDict["totalMoves"] - statsDict["totalHits"])
        hitMissRatio = str(round(hitMissRatio, 2))

      movesPerGame = statsDict["totalMoves"] / statsDict["totalGames"]
      movesPerGame = str(round(movesPerGame, 2))
      windowMessage = f"Win / loss ratio: {winLossRatio}\nAverage moves per game {movesPerGame}\nHit / miss ratio: {hitMissRatio}"
    else:
      windowMessage = "No statistics to display, play a game"

    #Display the message as a popup
    #Reuse the first screen found to send the popup from
    self.screens[self.namedScreenIds[list(self.namedScreenIds.keys())[0]]].showMessage(windowMessage)

class BattleshipsWindow(Window):
  def __init__(self, interfacePath, title):
    #Create a window, load the UI and connect signals
    super().__init__(interfacePath)
    self.setupWindow()
    self.setTitle(title)

    self.screens = []
    self.namedScreenIds = {}

    #Content elements
    self.content = self.builder.get_object("main-content")
    self.activeScreenId = None

    #Track an instance of the game
    self.game = Game(self)

  def createSetup(self, interfacePath):
    self.screens.append(screens.Setup(self, interfacePath))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    self.namedScreenIds["setup"] = screenId
    return screenId

  def createPlacement(self, interfacePath, playerId):
    self.screens.append(screens.Placement(self, interfacePath, playerId))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    self.namedScreenIds[f"placement-{playerId}"] = screenId
    return screenId

  def createBattlefield(self, interfacePath):
    self.screens.append(screens.Battlefield(self, interfacePath))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    self.namedScreenIds["battlefield"] = screenId
    return screenId

  def createGameEnd(self, interfacePath):
    self.screens.append(screens.GameEnd(self, interfacePath))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    self.namedScreenIds["game-end"] = screenId
    return screenId

  def setActiveScreen(self, screenId):
    if (self.activeScreenId != None):
      self.screens[self.activeScreenId].element.hide()
    self.screens[screenId].show()
    self.activeScreenId = screenId

  def reset(self):
    #Reset game, settings and opponent
    self.game.opponent = opponent.Opponent()
    for setting in self.game.gameSettings.keys():
      self.game.gameSettings[setting] = ""
    self.game.grids = []
    self.game.playerTurn = 0
    self.game.totalMoves = 0
    self.game.hitsMade = 0

    #Delete second player placement, if present
    if "placement-1" in self.namedScreenIds.keys():
      self.screens[self.namedScreenIds["placement-1"]] = None
      self.namedScreenIds.pop("placement-1")

    #Reset modified screens
    self.screens[self.namedScreenIds["placement-0"]] = None
    self.createPlacement("ui/placement.ui", 0)
    self.screens[self.namedScreenIds["battlefield"]] = None
    self.createBattlefield("ui/battlefields.ui")

    #Return to start screen
    self.setActiveScreen(self.namedScreenIds["setup"])

  def show(self):
    self.element.show()

class Game:
  def __init__(self, battleshipsWindow):
    self.gameSettings = {
      "opponent": "",
      "difficulty": "",
      "gamemode": ""
    }

    self.battleshipsWindow = battleshipsWindow
    self.grids = []
    self.battlefield = None

    self.opponent = opponent.Opponent()
    self.playerTurn = 0
    self.totalMoves = 0
    self.hitsMade = 0

  def start(self):
    battlefieldId = self.battleshipsWindow.namedScreenIds["battlefield"]
    self.battlefield = self.battleshipsWindow.screens[battlefieldId]

    if self.gameSettings["opponent"] == "computer":
      shipLengths = [5, 4, 3, 3, 2]
      if self.gameSettings["gamemode"] == "single-ship":
        shipLengths = [3, 3, 3, 3, 3]
      self.opponent.generateGrid(shipLengths)
      self.grids.append(self.opponent.grid)

      #Load weights if the opponent is a computer
      self.opponent.loadWeights(f"weights/weights-{self.gameSettings['difficulty']}.dmp")

      self.battlefield.rightPlayerLabel.set_label("Computer")
    else:
      self.battlefield.rightPlayerLabel.set_label("Guest")

    self.battlefield.setBoardInactive(0)

  def leftPlayerMove(self, position):
    #Check where that lands and update marker
    if self.grids[1][position[1]][position[0]] == 1: #Hit
      self.battlefield.setMarker(position, "right", "hit")

      #Increase hit counter and write to the board
      self.battlefield.increaseHitCounter("right")
      self.hitsMade += 1
      self.grids[1][position[1]][position[0]] = 0

      return True
    else: #Miss
      self.battlefield.setMarker(position, "right", "miss")
      return False

  def rightPlayerMove(self, position):
    #Check where that lands and update marker
    if self.grids[0][position[1]][position[0]] == 1: #Hit
      self.battlefield.setMarker(position, "left", "hit")

      #Increase hit counter and write to the board
      self.battlefield.increaseHitCounter("left")
      self.grids[0][position[1]][position[0]] = 0

      return True
    else: #Miss
      self.battlefield.setMarker(position, "left", "miss")
      return False

  def opponentMove(self):
    #Next turn (computer)
    guess = self.opponent.makeMove()

    #Check where that lands and update marker
    if self.grids[0][guess[1]][guess[0]] == 1: #Hit
      self.battlefield.setMarker(guess, "left", "hit")

      #Increase hit counter and write to the board
      self.battlefield.increaseHitCounter("left")
      self.grids[0][guess[1]][guess[0]] = 0
      self.opponent.feedbackMove("hit")

      return True
    else: #Miss
      self.battlefield.setMarker(guess, "left", "miss")
      self.opponent.feedbackMove("miss")
      return False

  def playerMove(self, position):
    wasHit = False
    if self.playerTurn == 0:
      wasHit = self.leftPlayerMove(position)
      self.totalMoves += 1

      #Check if the player won
      if self.checkWinner(self.grids[1]):
        self.handleWinner("Player 1")

      if self.gameSettings["opponent"] == "computer":
        #Check for an active streak
        if not (wasHit and self.gameSettings["gamemode"] == "streaks"):
          hitLoop = True
          while hitLoop:
            wasHit = self.opponentMove()
            self.battlefield.setBoardInactive(0)

            #Decide whether to give the computer another turn
            hitLoop = wasHit
            if self.gameSettings["gamemode"] != "streaks":
              hitLoop = False

            #Check if the computer won
            if self.checkWinner(self.grids[0]):
              self.handleWinner("Computer")
              hitLoop = False
      else:
        #Prepare board for right player
        self.playerTurn = 1
        self.battlefield.setBoardInactive(1)

    else:
      wasHit = self.rightPlayerMove(position)

      #Prepare board for left player
      self.playerTurn = 0
      self.battlefield.setBoardInactive(0)

      #Check if the right player won
      if self.checkWinner(self.grids[0]):
        self.handleWinner("Guest")

    if wasHit and self.gameSettings["gamemode"] == "streaks":
      #Flip which player's turn
      if self.gameSettings["opponent"] != "computer":
        self.playerTurn = 1 - self.playerTurn
        self.battlefield.setBoardInactive(self.playerTurn)

  def saveStatistics(self, totalMoves, hitsMade, playerWon):
    statsPath = "stats.csv"
    statsDict, foundFile = readStats(statsPath)

    #Update recorded statistics with new values
    if playerWon:
      statsDict["totalWins"] += 1
    statsDict["totalGames"] += 1
    statsDict["totalMoves"] += totalMoves
    statsDict["totalHits"] += hitsMade

    #Save new statistics to file
    with open(statsPath, "w+") as statsFile:
      for key in statsDict.keys():
        lineString = f"{key},{statsDict[key]}\n"
        statsFile.write(lineString)

  def handleWinner(self, winner):
    print(f"{winner} has won!")
    self.battlefield.showMessage(f"{winner} has won!")

    #Statistics recording
    playerWon = True if winner == "Player 1" else False
    self.saveStatistics(self.totalMoves, self.hitsMade, playerWon)

    gameEndScreenId = self.battleshipsWindow.namedScreenIds["game-end"]
    gameEndScreen = self.battleshipsWindow.screens[gameEndScreenId]

    self.battleshipsWindow.setActiveScreen(gameEndScreenId)
    gameEndScreen.setWinner(winner)
    gameEndScreen.setStatistics(self.totalMoves, self.hitsMade)

  def checkWinner(self, grid):
    for row in grid:
      for col in row:
        if col == 1:
          return False
    return True

  def placeShip(self, grid, shipLength, isRotated, position, gtkGrid = False):
    #Parse the position
    targetCol = position[0]
    targetRow = position[1]

    #Write the ship to the board
    if isRotated:
      for i in range(shipLength):
        grid[targetRow + i][targetCol] = 1
        if gtkGrid != False:
          gtkGrid.get_child_at(targetCol, targetRow + i).destroy()
          image = Gtk.Image.new_from_file("assets/placed.png")
          image.show()
          gtkGrid.attach(image, targetCol, targetRow + i, 1, 1)
    else:
      for i in range(shipLength):
        grid[targetRow][targetCol + i] = 1
        if gtkGrid != False:
          gtkGrid.get_child_at(targetCol + i, targetRow).destroy()
          image = Gtk.Image.new_from_file("assets/placed.png")
          image.show()
          gtkGrid.attach(image, targetCol + i, targetRow, 1, 1)
