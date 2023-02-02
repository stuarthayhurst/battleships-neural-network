#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#Container class for a Gtk Builder and a widget
class Element:
  def __init__(self, uiFilePath, elementName):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(uiFilePath)
    self.element = self.builder.get_object(elementName)

  #Show all main element and all its children
  def show(self):
    self.element.show_all()

#Class with common requirements for all shown screens
# - Contains common attributes and an instance of Element
# - Standardises creating each screen, easier to develop further
class Screen(Element):
  def __init__(self, battleshipsWindow, interfacePath, elementName):
    super().__init__(interfacePath, elementName)
    self.battleshipsWindow = battleshipsWindow
    self.parentWindow = battleshipsWindow.element
    self.namedScreenIds = battleshipsWindow.namedScreenIds
    self.game = battleshipsWindow.game

  #Send a blocking popup, requires the user to close the popup before execution resumes
  def showMessage(self, message):
    messageWindow = Gtk.MessageDialog(self.parentWindow, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
    messageWindow.run()
    messageWindow.destroy()

#Class to represent an individual tile on the ship placement
class Tile():
  def __init__(self, parentScreen, tileId):
    self.parentScreen = parentScreen
    self.tileId = int(tileId)

    #Create button and connect callback
    self.element = Gtk.Button.new_with_label("")
    self.element.connect("clicked", self.tilePressed)

  #Called when the tile is pressed, updates the currently selected tile on the parent screen
  def tilePressed(self, button):
    self.parentScreen.targetTile = self.tileId

#Class to represent an individual tile during gameplay
class GameTile():
  def __init__(self, parentScreen, tileId):
    self.parentScreen = parentScreen
    self.tileId = int(tileId)

    #Create button and connect callback
    self.element = Gtk.Button.new_with_label("")
    self.element.connect("clicked", self.tilePressed)

  #Called when the tile is pressed, triggers a player move on the parent screen
  def tilePressed(self, button):
    self.parentScreen.playerMove(self.tileId)
