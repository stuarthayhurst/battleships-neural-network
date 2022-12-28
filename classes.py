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
  def __init__(self, namedScreenIds, game, interfacePath, elementName):
    super().__init__(interfacePath, elementName)
    self.namedScreenIds = namedScreenIds
    self.game = game

class Tile():
  def __init__(self, tileId):
    self.tileId = tileId
    self.element = Gtk.Button.new_with_label("")
    self.element.connect("clicked", self.tilePressed)

    print(f"Created tile {self.tileId}")

  def tilePressed(self, button):
    print(f"Pressed tile {self.tileId}")
