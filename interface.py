#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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
    self.game = Game()

  def createSetup(self, interfacePath):
    self.screens.append(screens.Setup(self.namedScreenIds, self.game, interfacePath, self))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    self.namedScreenIds["setup"] = screenId
    return screenId

  def createPlacement(self, interfacePath):
    self.screens.append(screens.Placement(self.namedScreenIds, self.game, interfacePath))
    screenId = len(self.screens) - 1
    self.content.pack_start(self.screens[screenId].element, True, True, 0)
    self.screens[screenId].element.hide()

    self.namedScreenIds["placement"] = screenId
    return screenId

  def createBattlefield(self, interfacePath, size):
    self.screens.append(screens.Battlefield(self.namedScreenIds, self.game, interfacePath, size))
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

class Game:
  def __init__(self):
    self.gameSettings = {
      "opponent": "",
      "difficulty": "",
      "gamemode": ""
    }
