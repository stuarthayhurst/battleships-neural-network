#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import classes

class Setup(classes.Screen):
  def __init__(self, namedScreenIds, game, interfacePath, window):
    super().__init__(namedScreenIds, game, interfacePath, "setup")

    self.battleshipsWindow = window
    self.parentWindow = window.element
    self.opponentSelector = self.builder.get_object("opponent-multiplayer")
    self.difficultyArea = self.builder.get_object("difficulty-area")
    self.difficultyCombo = self.builder.get_object("difficulty-combo")
    self.gamemodeCombo = self.builder.get_object("gamemode-combo")
    self.startButton = self.builder.get_object("start-button")

    self.startButton.connect("clicked", self.startButtonPressed)
    self.opponentSelector.connect("toggled", self.opponentSelectorChanged)

  def showError(self, errorMessage):
    errorWindow = Gtk.MessageDialog(self.parentWindow, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, errorMessage)
    errorWindow.run()
    errorWindow.destroy()

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
      self.showError("You must select a difficulty")
      failed = True

    #Display an error if no game mode was selected
    if (gamemode == -1):
      self.showError("You must select a game mode")
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

    self.battleshipsWindow.setActiveScreen(self.namedScreenIds["placement"])

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
  def __init__(self, namedScreenPairs, game, interfacePath):
    super().__init__(namedScreenPairs, game, interfacePath, "placement")

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
        tile = classes.Tile(str((x * 7) + y))
        self.userBoard.attach(tile.element, x, y, 1, 1)

    self.ships = [self.builder.get_object(f"ship-{i + 1}") for i in range(5)]

    shipLengths = [5, 4, 3, 3, 2]
    for i in range(len(self.ships)):
      self.ships[i].add(self.createShipElement(shipLengths[i]))

  def rotateButtonPressed(self, button):
    print("Rotate pressed")
    print(self.game.gameSettings)

  def confirmButtonPressed(self, button):
    print("Confirm button pressed")

  def createShipElement(self, shipLength):
    container = Gtk.Box()
    for i in range(shipLength):
      piece = Gtk.Image.new_from_file("assets/placed.png")
      container.add(piece)

    return container

class Battlefield(classes.Screen):
  def __init__(self, namedScreenPairs, game, interfacePath, size):
    super().__init__(namedScreenPairs, game, interfacePath, "battlefield")

    for battlefield in self.element.get_children():
      for i in range(size):
        battlefield.insert_row(0)
        battlefield.insert_column(0)

      for x in range(size):
        for y in range(size):
          tile = classes.Tile(str((x * size) + y))
          battlefield.attach(tile.element, x, y, 1, 1)
