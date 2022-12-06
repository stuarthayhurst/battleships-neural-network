#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#Wrapper class for GTK
class Window:
  def __init__(self):
    self.builder = Gtk.Builder()
    self.window = None

  def loadFile(self, uiFilePath):
    self.builder.add_from_file(uiFilePath)

  def addWindow(self, windowElement, title = "Window"):
    self.window = self.builder.get_object(windowElement)

    #Create and set a header bar
    self.headerBar = Gtk.HeaderBar()
    self.headerBar.set_title(title)
    self.headerBar.set_show_close_button(True)
    self.window.set_titlebar(self.headerBar)

  def addSignalHandler(self, signalHandler):
    self.builder.connect_signals(signalHandler())

  def setTitle(self, title):
    self.headerBar.set_title(title)

  def showAll(self):
    self.window.show_all()

#Signal handler callbacks
class SignalHandler:
  def onDestroy(self, *args):
    print("Closed main window")
    Gtk.main_quit()

class BattleshipsWindow:
  def __init__(self, interfacePath, mainElement, title):
    #Create a window, load the UI and connect signals
    self.window = Window()
    self.window.loadFile(interfacePath)
    self.window.addWindow(mainElement)
    self.window.addSignalHandler(SignalHandler)
    self.window.setTitle(title)

  def buildGrid(self, elementId, size):
    for battlefield in self.window.builder.get_object(elementId).get_children():
    #battlefield = self.window.builder.get_object(elementId);
      for i in range(size):
        battlefield.insert_row(0)
        battlefield.insert_column(0)

      for x in range(size):
        for y in range(size):
          button = Gtk.Button.new_with_label(str((x * size) + y))
          battlefield.attach(button, x, y, 1, 1)

  def show(self):
    self.window.showAll()
