#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import classes
  
class Setup(classes.Screen):
  def __init__(self, namedScreenIds, interfacePath, window):
    super().__init__(namedScreenIds, interfacePath, "setup")

    self.parentWindow = window
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

    #Get value of difficulty selector
    difficulty = self.difficultyCombo.get_active()

    #Get value of game mode
    gamemode = self.gamemodeCombo.get_active()

    print("Game settings:")
    print(f" - Opponent: {opponent}")
    print(f" - Difficulty: {difficulty}")
    print(f" - Game mode: {gamemode}")

    #Display an error if playing against the computer with no difficulty selected
    if (difficulty == -1) and (opponent == "computer"):
      self.showError("You must select a difficulty")

    #Display an error if no game mode was selected
    if (gamemode == -1):
      self.showError("You must select a game mode")

  def opponentSelectorChanged(self, button):
    if (button.get_active()):
      self.difficultyArea.set_sensitive(False)
    else:
      self.difficultyArea.set_sensitive(True)

class Placement(classes.Screen):
  def __init__(self, namedScreenPairs, interfacePath):
    super().__init__(namedScreenPairs, interfacePath, "placement")

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

  def confirmButtonPressed(self, button):
    print("Confirm button pressed")

  def createShipElement(self, shipLength):
    container = Gtk.Box()
    for i in range(shipLength):
      piece = Gtk.Image.new_from_file("assets/placed.png")
      container.add(piece)

    return container

class Battlefield(classes.Screen):
  def __init__(self, namedScreenPairs, interfacePath, size):
    super().__init__(namedScreenPairs, interfacePath, "battlefield")

    for battlefield in self.element.get_children():
      for i in range(size):
        battlefield.insert_row(0)
        battlefield.insert_column(0)

      for x in range(size):
        for y in range(size):
          tile = classes.Tile(str((x * size) + y))
          battlefield.attach(tile.element, x, y, 1, 1)
