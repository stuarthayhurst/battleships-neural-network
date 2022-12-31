#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import interface

#Setup window
window = interface.BattleshipsWindow("ui/main-window.ui", "Battleships")
setupId = window.createSetup("ui/setup.ui")
placementId = window.createPlacement("ui/placement.ui", 0)
battlefieldId = window.createBattlefield("ui/battlefields.ui")

window.setActiveScreen(setupId)

#Show the window and start the mainloop
window.element.connect("destroy", Gtk.main_quit)
window.show()
Gtk.main()
