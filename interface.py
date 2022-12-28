#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Element:
  def __init__(self, uiFilePath, elementName):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(uiFilePath)
    self.element = self.builder.get_object(elementName)

  def show(self):
    self.element.show_all()

#Wrapper class for GTK
class Window(Element):
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

class Setup(Element):
  def __init__(self, interfacePath, window):
    super().__init__(interfacePath, "setup")

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

class Placement(Element):
  def __init__(self, interfacePath):
    super().__init__(interfacePath, "placement")

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
        tile = Tile(str((x * 7) + y))
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

class Tile():
  def __init__(self, tileId):
    self.tileId = tileId
    self.element = Gtk.Button.new_with_label("")
    self.element.connect("clicked", self.tilePressed)

    print(f"Created tile {self.tileId}")

  def tilePressed(self, button):
    print(f"Pressed tile {self.tileId}")

class Battlefield(Element):
  def __init__(self, interfacePath, size):
    super().__init__(interfacePath, "battlefield")

    for battlefield in self.element.get_children():
      for i in range(size):
        battlefield.insert_row(0)
        battlefield.insert_column(0)

      for x in range(size):
        for y in range(size):
          tile = Tile(str((x * size) + y))
          battlefield.attach(tile.element, x, y, 1, 1)

class BattleshipsWindow(Window):
  def __init__(self, interfacePath, title):
    #Create a window, load the UI and connect signals
    super().__init__(interfacePath)
    self.setupWindow()
    self.setTitle(title)

    self.screens = []

    #Content elements
    self.content = self.builder.get_object("main-content")
    self.activeScreenId = None

  def createSetup(self, interfacePath):
    self.screens.append(Setup(interfacePath, self.element))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    return screenId

  def createPlacement(self, interfacePath):
    self.screens.append(Placement(interfacePath))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    return screenId

  def createBattlefield(self, interfacePath, size):
    self.screens.append(Battlefield(interfacePath, size))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    return screenId

  def setActiveScreen(self, screenId):
    if (self.activeScreenId != None):
      self.screens[self.activeScreenId].element.hide()
    self.screens[screenId].show()
    self.activeScreenId = screenId

  def show(self):
    self.element.show()
