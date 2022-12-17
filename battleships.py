#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import interface

#Create window, set title and begin event loop
window = interface.BattleshipsWindow("ui/main-window.ui", "Battleships")
window.createBattlefield("ui/battlefields.ui", 7)

window.setBattlefieldActive()

window.show()
Gtk.main()



#Add validation to passed params
