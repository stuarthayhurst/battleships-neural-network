#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import classes

class Setup(classes.Screen):
  def __init__(self, battleshipsWindow, interfacePath):
    super().__init__(battleshipsWindow, interfacePath, "setup")

    self.opponentSelector = self.builder.get_object("opponent-multiplayer")
    self.difficultyArea = self.builder.get_object("difficulty-area")
    self.difficultyCombo = self.builder.get_object("difficulty-combo")
    self.gamemodeCombo = self.builder.get_object("gamemode-combo")
    self.startButton = self.builder.get_object("start-button")

    self.startButton.connect("clicked", self.startButtonPressed)
    self.opponentSelector.connect("toggled", self.opponentSelectorChanged)

  def startButtonPressed(self, button):
    #Get value of opponent selector
    opponent = "computer"
    if (self.opponentSelector.get_active()):
      opponent = "multiplayer"

    #Get value of difficulty selector and game mode
    difficulty = self.difficultyCombo.get_active()
    gamemode = self.gamemodeCombo.get_active()
    failed = False

    #Display an error if playing against the computer with no difficulty selected
    if (difficulty == -1) and (opponent == "computer"):
      self.showMessage("You must select a difficulty")
      failed = True

    #Display an error if no game mode was selected
    if (gamemode == -1):
      self.showMessage("You must select a game mode")
      failed = True

    if failed:
      return

    #Dictionaries to convert numbered settings to strings
    translateDifficulty = {
      0: "easy",
      1: "normal",
      2: "hard"
    }
    translateGamemode = {
      0: "normal",
      1: "streaks",
      2: "single-ship",
      3: "powerups"
    }

    self.game.gameSettings["opponent"] = opponent
    if (opponent == "multiplayer"):
      self.game.gameSettings["difficulty"] = "none"
    else:
      self.game.gameSettings["difficulty"] = translateDifficulty[difficulty]
    self.game.gameSettings["gamemode"] = translateGamemode[gamemode]

    self.battleshipsWindow.setActiveScreen(self.namedScreenIds["placement-0"])

    print("Game settings:")
    print(f" - Opponent: {opponent}")
    print(f" - Difficulty: {difficulty}")
    print(f" - Game mode: {gamemode}")

  def opponentSelectorChanged(self, button):
    if (button.get_active()):
      self.difficultyArea.set_sensitive(False)
    else:
      self.difficultyArea.set_sensitive(True)

class Placement(classes.Screen):
  def __init__(self, battleshipsWindow, interfacePath, playerId):
    super().__init__(battleshipsWindow, interfacePath, "placement")
    self.isActiveShipRotated = False
    self.activeShipIndex = 0
    self.targetTile = -1
    self.playerId = playerId
    self.interfacePath = interfacePath

    #Accessed by [row][column]
    self.grid = [[0 for i in range(7)] for j in range(7)]

    self.rotateButton = self.builder.get_object("rotate-button")
    self.confirmButton = self.builder.get_object("confirm-button")

    image = Gtk.Image.new_from_file("assets/rotate.png")
    self.rotateButton.set_image(image)

    self.rotateButton.connect("clicked", self.rotateButtonPressed)
    self.confirmButton.connect("clicked", self.confirmButtonPressed)

    self.userBoard = self.builder.get_object("user-board")
    for i in range(7):
      self.userBoard.insert_row(0)
      self.userBoard.insert_column(0)

    for x in range(7):
      for y in range(7):
        tile = classes.Tile(self, str((x * 7) + y))
        self.userBoard.attach(tile.element, x, y, 1, 1)

    self.ships = [self.builder.get_object(f"ship-{i + 1}") for i in range(5)]
    self.shipRotateIcons = []

  def placeRemainingShips(self, shipLengths):
    self.shipLengths = shipLengths
    for i in range(len(self.ships)):
      self.ships[i].add(self.createShipElement(self.shipLengths[i]))
      #Reuse image from rotate button
      self.shipRotateIcons.append(Gtk.Image.new_from_file("assets/rotate.png"))
      self.ships[i].add(self.shipRotateIcons[i])

  def show(self):
    #Show the correct number of ships to be placed, depending on the game mode
    shipLengths = [5, 4, 3, 3, 2]
    if self.game.gameSettings["gamemode"] == "single-ship":
      shipLengths = [3, 3, 3, 3, 3]
    self.placeRemainingShips(shipLengths)

    #Show relevant elements
    self.element.show_all()
    for i in range(len(self.shipRotateIcons)):
      self.shipRotateIcons[i].hide()

  def updateActiveShipRotated(self):
    if self.activeShipIndex == len(self.shipLengths):
      return

    if self.isActiveShipRotated:
      self.shipRotateIcons[self.activeShipIndex].show()
    else:
      self.shipRotateIcons[self.activeShipIndex].hide()

  def rotateButtonPressed(self, button):
    self.isActiveShipRotated = not self.isActiveShipRotated
    self.updateActiveShipRotated()

  def confirmButtonPressed(self, button):
    if self.activeShipIndex == len(self.shipLengths):
      self.game.grids.append(self.grid)
      if self.game.gameSettings["opponent"] == "multiplayer" and self.playerId == 0:
        newPlacementId = self.battleshipsWindow.createPlacement(self.interfacePath, 1)
        self.battleshipsWindow.setActiveScreen(newPlacementId)
      else:
        self.battleshipsWindow.setActiveScreen(self.namedScreenIds["battlefield"])
      return

    if self.targetTile == -1:
      self.showMessage("You must select a tile to place the ship")
      return

    shipLength = self.shipLengths[self.activeShipIndex]

    self.targetTile = self.targetTile
    targetCol = self.targetTile // 7
    targetRow = self.targetTile % 7

    #Check ship fits within the board
    if self.isActiveShipRotated:
      if targetRow + (shipLength) > 7:
        self.showMessage("Invalid location, ship won't fit on the board")
        return
    else:
      if targetCol + (shipLength) > 7:
        self.showMessage("Invalid location, ship won't fit on the board")
        return

    #Check the ship doesn't collide with an existing ship
    if self.isActiveShipRotated:
      for i in range(shipLength):
        if self.grid[targetRow + i][targetCol] == 1:
          self.showMessage("Invalid location, ship would collide with another ship")
          return
    else:
      for i in range(shipLength):
        if self.grid[targetRow][targetCol + i] == 1:
          self.showMessage("Invalid location, ship would collide with another ship")
          return

    #Hide the currently active ship and rotate symbol from the menu
    self.ships[self.activeShipIndex].hide()
    self.shipRotateIcons[self.activeShipIndex].hide()

    #Write the active ship to the board
    self.game.placeShip(self.grid, shipLength, self.isActiveShipRotated, [targetCol, targetRow], self.userBoard)

    #Select the next ship
    self.activeShipIndex += 1

    #Reset the ship rotation and target tile
    self.isActiveShipRotated = False
    self.targetTile = -1

  def createShipElement(self, shipLength):
    container = Gtk.Box()
    for i in range(shipLength):
      piece = Gtk.Image.new_from_file("assets/placed.png")
      container.add(piece)

    return container

class Battlefield(classes.Screen):
  def __init__(self, battleshipsWindow, interfacePath):
    super().__init__(battleshipsWindow, interfacePath, "battlefield")

    self.leftGrid = self.builder.get_object("battlefield-left")
    self.rightGrid = self.builder.get_object("battlefield-right")

    self.hitCount = {
      "left": 0,
      "right": 0
    }

    self.powerUpLeft = self.builder.get_object("powerup-bar-left")
    self.powerUpRight = self.builder.get_object("powerup-bar-right")

    self.rightPlayerLabel = self.builder.get_object("name-label-right") 

    powerUpFiles = ["assets/carpetbomb.png", "assets/airstrike.png", "assets/cross.png"]
    powerUpCallbacks = [self.carpetbombPressed, self.airstrikePressed, self.crossPressed]

    for powerUpBar in [self.powerUpLeft, self.powerUpRight]:
      count = 0
      powerUpBar.set_sensitive(False)
      for powerUpButton in powerUpBar:
        powerUpButton.connect("clicked", powerUpCallbacks[count])
        image = Gtk.Image.new_from_file(powerUpFiles[count])
        powerUpButton.set_image(image)
        powerUpButton.set_sensitive(False)

        count += 1

    for battlefield in [self.leftGrid, self.rightGrid]:
      for i in range(7):
        battlefield.insert_row(0)
        battlefield.insert_column(0)

      for x in range(7):
        for y in range(7):
          tile = classes.GameTile(self, str((x * 7) + y))
          battlefield.attach(tile.element, x, y, 1, 1)

  def playerMove(self, tileId):
    position = [tileId // 7, tileId % 7]
    self.game.playerMove(position)

  def increaseHitCounter(self, side):
    self.hitCount[side] += 1
    self.builder.get_object(f"hit-counter-{side}").set_label(f"Hits: {self.hitCount[side]}")

  def setMarker(self, position, gridName, assetName):
    targetGrid = None
    if gridName == "left":
      targetGrid = self.leftGrid
    else:
      targetGrid = self.rightGrid

    targetGrid.get_child_at(position[0], position[1]).destroy()
    image = Gtk.Image.new_from_file(f"assets/{assetName}.png")
    image.show()
    targetGrid.attach(image, position[0], position[1], 1, 1)

  def setBoardInactive(self, boardNum):
    if boardNum == 0:
      self.leftGrid.set_sensitive(False)
      self.rightGrid.set_sensitive(True)
    else:
      self.rightGrid.set_sensitive(False)
      self.leftGrid.set_sensitive(True)

  def placeUserShips(self):
    rowCount = 0
    for row in self.game.grids[0]:
      colCount = 0
      for col in row:
        if col == 1:
          self.setMarker([colCount, rowCount], "left", "placed")
        colCount += 1
      rowCount += 1

  def show(self):
    if self.game.gameSettings["opponent"] == "computer":
      self.placeUserShips()
    self.element.show_all()
    self.game.start()

  def carpetbombPressed(self, button):
    print("Carpet bomb pressed")
    pass

  def airstrikePressed(self, button):
    print("Air strike pressed")
    pass

  def crossPressed(self, button):
    print("Cross pressed")
    pass

class GameEnd(classes.Screen):
  def __init__(self, battleshipsWindow, interfacePath):
    super().__init__(battleshipsWindow, interfacePath, "game-end")

    self.builder.get_object("quit-button").connect("clicked", self.quitButtonPressed)
    self.builder.get_object("restart-button").connect("clicked", self.restartButtonPressed)

  def quitButtonPressed(self, button):
    print("Quit pressed")

  def restartButtonPressed(self, button):
    print("Play again pressed")
