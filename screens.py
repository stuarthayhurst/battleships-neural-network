#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import classes

#Class to contain the setup screen widget and related methods
class Setup(classes.Screen):
  def __init__(self, battleshipsWindow, interfacePath):
    super().__init__(battleshipsWindow, interfacePath, "setup")

    #Get access to required Gtk objects
    self.opponentSelector = self.builder.get_object("opponent-multiplayer")
    self.difficultyArea = self.builder.get_object("difficulty-area")
    self.difficultyCombo = self.builder.get_object("difficulty-combo")
    self.gamemodeCombo = self.builder.get_object("gamemode-combo")
    self.startButton = self.builder.get_object("start-button")

    #Connect the buttons to their handlers
    self.startButton.connect("clicked", self.startButtonPressed)
    self.opponentSelector.connect("toggled", self.opponentSelectorChanged)

  #Callback function when the settings are confirmed
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
    }

    #Save the opponent, difficulty and game mode settings on the game instance
    self.game.gameSettings["opponent"] = opponent
    if (opponent == "multiplayer"):
      self.game.gameSettings["difficulty"] = "none"
    else:
      self.game.gameSettings["difficulty"] = translateDifficulty[difficulty]
    self.game.gameSettings["gamemode"] = translateGamemode[gamemode]

    #Set the ship placement screen as active
    self.battleshipsWindow.setActiveScreen(self.namedScreenIds["placement-0"])

    #Print the game settings chosen, for future reference
    print("Game settings:")
    print(f" - Opponent: {opponent}")
    print(f" - Difficulty: {difficulty}")
    print(f" - Game mode: {gamemode}")

  #Callback when opponent is changed
  # - Used to grey out difficulty if playing against a person
  def opponentSelectorChanged(self, button):
    #If the active option is multiplayer, set the difficulty as inactive
    if (button.get_active()):
      self.difficultyArea.set_sensitive(False)
    else:
      self.difficultyArea.set_sensitive(True)

#Class to represent placement screen widget and relevant methods
class Placement(classes.Screen):
  def __init__(self, battleshipsWindow, interfacePath, playerId):
    super().__init__(battleshipsWindow, interfacePath, "placement")
    self.isActiveShipRotated = False
    self.activeShipIndex = 0
    self.targetTile = -1
    self.playerId = playerId
    self.interfacePath = interfacePath

    #Structure to store user placed ships in
    #Accessed by [row][column]
    self.grid = [[0 for i in range(7)] for j in range(7)]

    playerName = "Player"
    if self.playerId == 1:
      playerName = "Guest"

    self.builder.get_object("player-ship-label").set_label(f"{playerName}'s ships")

    self.rotateButton = self.builder.get_object("rotate-button")
    self.confirmButton = self.builder.get_object("confirm-button")

    #Add rotate icon to rotate button
    image = Gtk.Image.new_from_file("assets/rotate.png")
    self.rotateButton.set_image(image)

    #Connect rotate and confirm buttons to their callbacks
    self.rotateButton.connect("clicked", self.rotateButtonPressed)
    self.confirmButton.connect("clicked", self.confirmButtonPressed)

    #Grow the grid to the right size
    self.userBoard = self.builder.get_object("user-board")
    for i in range(7):
      self.userBoard.insert_row(0)
      self.userBoard.insert_column(0)

    #Fill the grid with Tile instances, used to display the grid and take user inputs through their callbacks
    for x in range(7):
      for y in range(7):
        tile = classes.Tile(self, str((x * 7) + y))
        self.userBoard.attach(tile.element, x, y, 1, 1)

    #Record the remaining ships, for reference
    self.ships = [self.builder.get_object(f"ship-{i + 1}") for i in range(5)]
    self.shipRotateIcons = []

  #Fill the side bar with the ships left to place, according to shipLengths
  def placeRemainingShips(self, shipLengths):
    self.shipLengths = shipLengths
    #Iterate over ships to place
    for i in range(len(self.ships)):
      #Create a container for each ship, filled with a number of markers
      self.ships[i].add(self.createShipElement(self.shipLengths[i]))
      #Reuse image from rotate button
      self.shipRotateIcons.append(Gtk.Image.new_from_file("assets/rotate.png"))
      self.ships[i].add(self.shipRotateIcons[i])

  #Function to show the screen, special handling to avoid showing hidden ships
  # - Ships are hidden on the left when placed, show_all() would reveal these if they weren't tracked and handled
  def show(self):
    #Show the correct number of ships to be placed, depending on the game mode
    shipLengths = [5, 4, 3, 3, 2]
    if self.game.gameSettings["gamemode"] == "single-ship":
      shipLengths = [3, 3, 3, 3, 3]
    self.placeRemainingShips(shipLengths)

    #Highlight the first ship
    self.setNextShipActive()

    #Show relevant elements
    self.element.show_all()
    for i in range(len(self.shipRotateIcons)):
      self.shipRotateIcons[i].hide()

  #Show or hide to rotation symbol next to the ship to place
  def updateActiveShipRotated(self):
    if self.activeShipIndex == len(self.shipLengths):
      return

    if self.isActiveShipRotated:
      self.shipRotateIcons[self.activeShipIndex].show()
    else:
      self.shipRotateIcons[self.activeShipIndex].hide()

  def setNextShipActive(self):
    #Set all markers in the next ship to active
    if self.activeShipIndex != len(self.shipLengths):
      for image in self.ships[self.activeShipIndex].get_children()[0].get_children():
        image.set_sensitive(True)

  #Callback when rotating the ship, update the state and call update function
  def rotateButtonPressed(self, button):
    self.isActiveShipRotated = not self.isActiveShipRotated
    self.updateActiveShipRotated()

  #Callback for confirm button
  # - If all ships have been placed, move to the next screen
  #   - If playing multiplayer, place the second user's ships
  #   - If playing against the computer or the second user's ships are placed, start te game
  # - Validate the selected position
  # - Place the ship if valid, otherwise send a warning
  def confirmButtonPressed(self, button):
    #If all ships have been placed, either start placing ships for the second player or start the game
    if self.activeShipIndex == len(self.shipLengths):
      self.game.grids.append(self.grid)
      if self.game.gameSettings["opponent"] == "multiplayer" and self.playerId == 0:
        newPlacementId = self.battleshipsWindow.createPlacement(self.interfacePath, 1)
        self.battleshipsWindow.setActiveScreen(newPlacementId)
      else:
        self.battleshipsWindow.setActiveScreen(self.namedScreenIds["battlefield"])
      return

    #Validate a tile has been selected, send a warning if not
    if self.targetTile == -1:
      self.showMessage("You must select a tile to place the ship")
      return

    shipLength = self.shipLengths[self.activeShipIndex]

    #Convert tile index to a grid coordinate
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

    #Brighten the next ship
    self.setNextShipActive()

    #Reset the ship rotation and target tile
    self.isActiveShipRotated = False
    self.targetTile = -1

  #Create a Gtk Box, fill it with markers and return it
  def createShipElement(self, shipLength):
    container = Gtk.Box()
    for i in range(shipLength):
      piece = Gtk.Image.new_from_file("assets/placed.png")
      container.add(piece)

      #By default, grey out the piece
      piece.set_sensitive(False)

    return container

#Class to represent the battlefield widget and its methods
class Battlefield(classes.Screen):
  def __init__(self, battleshipsWindow, interfacePath):
    super().__init__(battleshipsWindow, interfacePath, "battlefield")

    #Access left and right playing fields
    self.leftGrid = self.builder.get_object("battlefield-left")
    self.rightGrid = self.builder.get_object("battlefield-right")

    #Track hit counts for each player
    self.hitCount = {
      "left": 0,
      "right": 0
    }

    self.rightPlayerLabel = self.builder.get_object("name-label-right") 

    #Add rows, columns and clickable tiles for both battlefields
    for battlefield in [self.leftGrid, self.rightGrid]:
      for i in range(7):
        battlefield.insert_row(0)
        battlefield.insert_column(0)

      for x in range(7):
        for y in range(7):
          tile = classes.GameTile(self, str((x * 7) + y))
          battlefield.attach(tile.element, x, y, 1, 1)

  #Callback when tile clicked
  # - Convert tile index to coordinate
  # - Forward call to running game
  def playerMove(self, tileId):
    position = [tileId // 7, tileId % 7]
    self.game.playerMove(position)

  #Increase the saved number of hits for an operator, display the new data
  def increaseHitCounter(self, side):
    self.hitCount[side] += 1
    self.builder.get_object(f"hit-counter-{side}").set_label(f"Hits: {self.hitCount[side]}")

  #Sets the specified location on the specified grid to the specified marker (hit, miss, placement)
  def setMarker(self, position, gridName, assetName):
    #Select the correct grid
    targetGrid = None
    if gridName == "left":
      targetGrid = self.leftGrid
    else:
      targetGrid = self.rightGrid

    #Find the target location and update the element
    targetGrid.get_child_at(position[0], position[1]).destroy()
    image = Gtk.Image.new_from_file(f"assets/{assetName}.png")
    image.show()
    targetGrid.attach(image, position[0], position[1], 1, 1)

  #Grey out the specified board
  def setBoardInactive(self, boardNum):
    if boardNum == 0:
      self.leftGrid.set_sensitive(False)
      self.rightGrid.set_sensitive(True)
    else:
      self.rightGrid.set_sensitive(False)
      self.leftGrid.set_sensitive(True)

  #Function to reveal the user's ships on the left for reference, when in singleplayer mode
  def placeUserShips(self):
    rowCount = 0
    for row in self.game.grids[0]:
      colCount = 0
      for col in row:
        if col == 1:
          self.setMarker([colCount, rowCount], "left", "placed")
        colCount += 1
      rowCount += 1

  #Special handling for show()
  # - Called when game should start
  # - Show user ships if needed
  # - Show all elements
  # - Trigger the game to start
  def show(self):
    if self.game.gameSettings["opponent"] == "computer":
      self.placeUserShips()
    self.element.show_all()
    self.game.start()

#Class to contain game end widget and methods
class GameEnd(classes.Screen):
  def __init__(self, battleshipsWindow, interfacePath):
    super().__init__(battleshipsWindow, interfacePath, "game-end")

    self.winnerLabel = self.builder.get_object("winner-label")
    self.statisticsLabel = self.builder.get_object("statistics-label")

    #Connect buttons to callbacks
    self.builder.get_object("quit-button").connect("clicked", self.quitButtonPressed)
    self.builder.get_object("restart-button").connect("clicked", self.restartButtonPressed)

  #Update the winner
  def setWinner(self, winner):
    self.winnerLabel.set_label(f"{winner} has won!")

  #Calculate and update the displayed statistics
  def setStatistics(self, guessCount, hitCount):
    ratio = hitCount / (guessCount - hitCount)
    self.statisticsLabel.set_label(f"Guesses made: {guessCount}\nHits made: {hitCount}\nHit / miss ratio {round(ratio, 2)}")

  #Callback for user requesting to quit (button)
  def quitButtonPressed(self, button):
    Gtk.main_quit()

  #Callback for user requesting a restart (button)
  def restartButtonPressed(self, button):
    #Trigger reset on the program
    self.battleshipsWindow.reset()
