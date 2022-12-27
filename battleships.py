#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import interface

#Create window, set title and begin event loop
window = interface.BattleshipsWindow("ui/main-window.ui", "Battleships")

setupId = window.createSetup("ui/setup.ui")
battlefieldId = window.createBattlefield("ui/battlefields.ui", 7)

window.setActiveScreen(setupId)

window.element.connect("destroy", Gtk.main_quit)

window.show()
Gtk.main()



#Add validation to passed params
