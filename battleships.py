#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import interface

#Create window, set title and begin event loop
window = interface.BattleshipsWindow("main-window.ui", "main-window", "Battleships")
window.buildGrid('battlefield', 7)

window.show()
Gtk.main()



#Add validation to passed params
