#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import opponent
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
    else: #Miss
      self.battlefield.setMarker(position, "right", "miss")

  def rightPlayerMove(self, position):
    #Check where that lands and update marker
    if self.grids[0][position[1]][position[0]] == 1: #Hit
      self.battlefield.setMarker(position, "left", "hit")

      #Increase hit counter and write to the board
      self.battlefield.increaseHitCounter("left")
      self.grids[0][position[1]][position[0]] = 0
    else: #Miss
      self.battlefield.setMarker(position, "left", "miss")

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
    else: #Miss
      self.battlefield.setMarker(guess, "left", "miss")
      self.opponent.feedbackMove("miss")

  def playerMove(self, position):
    if self.playerTurn == 0:
      self.leftPlayerMove(position)
      self.totalMoves += 1

      #Check if the player won
      if self.checkWinner(self.grids[1]):
        self.handleWinner("Player 1")

      if self.gameSettings["opponent"] == "computer":
        self.opponentMove()
        self.battlefield.setBoardInactive(0)

        #Check if the computer won
        if self.checkWinner(self.grids[0]):
          self.handleWinner("Computer")
      else:
        #Prepare board for right player
        self.playerTurn = 1
        self.battlefield.setBoardInactive(1)

    else:
      self.rightPlayerMove(position)

      #Prepare board for left player
      self.playerTurn = 0
      self.battlefield.setBoardInactive(0)

      #Check if the right player won
      if self.checkWinner(self.grids[0]):
        self.handleWinner("Guest")

  def handleWinner(self, winner):
    print(f"{winner} has won!")
    self.battlefield.showMessage(f"{winner} has won!")

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
