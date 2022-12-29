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

class Screen(Element):
  def __init__(self, battleshipsWindow, interfacePath, elementName):
    super().__init__(interfacePath, elementName)
    self.battleshipsWindow = battleshipsWindow
    self.parentWindow = battleshipsWindow.element
    self.namedScreenIds = battleshipsWindow.namedScreenIds
    self.game = battleshipsWindow.game

  def showError(self, errorMessage):
    errorWindow = Gtk.MessageDialog(self.parentWindow, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, errorMessage)
    errorWindow.run()
    errorWindow.destroy()

class Tile():
  def __init__(self, parentScreen, tileId):
    self.parentScreen = parentScreen
    self.tileId = tileId
    self.element = Gtk.Button.new_with_label("")
    self.element.connect("clicked", self.tilePressed)

  def tilePressed(self, button):
    self.parentScreen.targetTile = int(self.tileId)
