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

  def setupWindow(self):
    #Create and set a header bar
    self.headerBar = Gtk.HeaderBar()
    self.headerBar.set_title("Window")
    self.headerBar.set_show_close_button(True)
    self.headerBar.show_all()
    self.element.set_titlebar(self.headerBar)

    #Add icons to buttons
    image = Gtk.Image.new_from_file("assets/sound-on.png")
    self.builder.get_object("sound-toggle-button").set_image(image)

    image = Gtk.Image.new_from_file("assets/statistics.png")
    self.builder.get_object("statistics-button").set_image(image)

    image = Gtk.Image.new_from_file("assets/achievements.png")
    self.builder.get_object("achievements-button").set_image(image)

  def addSignalHandler(self, signalHandler):
    self.builder.connect_signals(signalHandler())

  def setTitle(self, title):
    self.headerBar.set_title(title)

#Signal handler callbacks
class SignalHandler:
  def onDestroy(self, *args):
    print("Closed main window")
    Gtk.main_quit()

class Tile(Gtk.Button):
  def __init__(self, n):
    self.element = Gtk.Button.new_with_label(n)
    print(f"Created tile {n}")

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

class Setup(Element):
  def __init__(self, interfacePath):
    super().__init__(interfacePath, "setup")

class BattleshipsWindow(Window):
  def __init__(self, interfacePath, title):
    #Create a window, load the UI and connect signals
    super().__init__(interfacePath)
    self.setupWindow()
    self.addSignalHandler(SignalHandler)
    self.setTitle(title)

    self.screens = []

    #Content elements
    self.content = self.builder.get_object("main-content")
    self.activeScreenId = None

  def createSetup(self, interfacePath):
    self.screens.append(Setup(interfacePath))
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
