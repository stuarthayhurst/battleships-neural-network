#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import random, time

import screens
import classes

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

    #Add icons to buttons and connect signals
    image = Gtk.Image.new_from_file("assets/sound-on.png")
    soundButton = self.builder.get_object("sound-toggle-button")
    soundButton.set_image(image)
    soundButton.connect("clicked", self.soundTogglePressed)

    image = Gtk.Image.new_from_file("assets/statistics.png")
    statsButton = self.builder.get_object("statistics-button")
    statsButton.set_image(image)
    statsButton.connect("clicked", self.statsButtonPressed)

    image = Gtk.Image.new_from_file("assets/achievements.png")
    achievementsButton = self.builder.get_object("achievements-button")
    achievementsButton.set_image(image)
    achievementsButton.connect("clicked", self.achievementsButtonPressed)

  def soundTogglePressed(self, button):
    print("Sound toggle pressed")

  def statsButtonPressed(self, button):
    print("Statistics button pressed")

  def achievementsButtonPressed(self, button):
    print("Achievements button pressed")

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

  def createPlacement(self, interfacePath):
    self.screens.append(screens.Placement(self, interfacePath))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    self.namedScreenIds["placement"] = screenId
    return screenId

  def createBattlefield(self, interfacePath):
    self.screens.append(screens.Battlefield(self, interfacePath))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    self.namedScreenIds["battlefield"] = screenId
    return screenId

  def setActiveScreen(self, screenId):
    if (self.activeScreenId != None):
      self.screens[self.activeScreenId].element.hide()
    self.screens[screenId].show()
    self.activeScreenId = screenId

  def show(self):
    self.element.show()

class Opponent():
  def __init__(self):
    self.grid = [[0 for i in range(7)] for j in range(7)]
    self.enemyGrid = [[0 for i in range(7)] for j in range(7)]

    self.lastGuess = []

  def feedbackMove(self, result):
    if result == "hit":
      self.enemyGrid[self.lastGuess[1]][self.lastGuess[0]] = 1
    else:
      self.enemyGrid[self.lastGuess[1]][self.lastGuess[0]] = -1

  def makeMove(self):
    guessing = True
    x, y = 0, 0
    while guessing:
      x = random.randint(0, 6)
      y = random.randint(0, 6)

      if self.enemyGrid[y][x] == 0:
        guessing = False

    self.lastGuess = [x, y]
    return [x, y]

  def generateGrid(self, shipLengths):
    #Fill the grids with ships
    for shipLength in shipLengths:
      #Keep trying to place until it succeeds
      placing = True
      while placing:
        #Generate position
        flipped = bool(random.randint(0, 1))
        x, y = random.randint(0, 6), random.randint(0, 6)

        #Attempt to place the piece
        if self.placePiece(shipLength, x, y, flipped):
          placing = False

  def placePiece(self, length, x, y, flipped):
    #Return false if the ship won't fit
    if not flipped:
      if x + length > len(self.grid[0]):
        return False
    else:
      if y + length > len(self.grid):
        return False

    #Return false if another ship is in the way
    if not flipped:
      for i in range(x, x + length):
        if self.grid[y][i] != 0:
          return False
    else:
      for i in range(y, y + length):
        if self.grid[i][x] != 0:
          return False

    #Place the ship on the grid
    if not flipped:
      for i in range(x, x + length):
        self.grid[y][i] = 1
    else:
      for i in range(y, y + length):
        self.grid[i][x] = 1

    return True

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

    self.opponent = Opponent()

  def start(self):
    battlefieldId = self.battleshipsWindow.namedScreenIds["battlefield"]
    self.battlefield = self.battleshipsWindow.screens[battlefieldId]

    if self.gameSettings["opponent"] == "computer":
      shipLengths = [5, 4, 3, 3, 2]
      if self.gameSettings["gamemode"] == "single-ship":
        shipLengths = [3, 3, 3, 3, 3]
      self.opponent.generateGrid(shipLengths)
      self.grids.append(self.opponent.grid)

    self.battlefield.setLeftBoardInactive()

  def playerMove(self, position):
    #Check where that lands and update marker
    if self.grids[1][position[1]][position[0]] == 1: #Hit
      self.battlefield.setMarker(position, "right", "hit")

      #Increase hit counter and write to the board
      self.battlefield.increaseHitCounter("right")
      self.grids[1][position[1]][position[0]] = 0
    else: #Miss
      self.battlefield.setMarker(position, "right", "miss")

    #Check for a winner
    if self.checkWinner(self.grids[1]):
      print("Player has won")

    #Next turn (computer)
    self.battlefield.setRightBoardInactive()
    guess = self.opponent.makeMove()

    #Check where that lands and update marker
    if self.grids[0][guess[1]][guess[0]] == 1: #Hit
      self.battlefield.setMarker(guess, "left", "hit")

      #Increase hit counter and write to the board
      self.battlefield.increaseHitCounter("left")
      self.grids[0][guess[1]][guess[0]] = 0
      self.opponent.feedbackMove("hit")
    else: #Miss
      self.battlefield.setMarker(guess, "left", "miss")
      self.opponent.feedbackMove("miss")

    if self.checkWinner(self.grids[0]):
      print("Computer has won")

    #Prepare for next player turn
    self.battlefield.setLeftBoardInactive()

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
