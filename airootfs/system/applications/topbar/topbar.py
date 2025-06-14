#!/usr/bin/env python3
import gi
import datetime

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from pywlroots import WlrootsCompositor, LayerShellV1

class TopBar:
    def __init__(self):
        self.compositor = WlrootsCompositor()
        self.layershell = LayerShellV1(self.compositor)

        self.compositor.start()

        # GTK app and window
        self.app = Gtk.Application(application_id="com.drawsko.TopBar")
        self.app.connect("activate", self.on_activate)

    def on_activate(self, app):
        # Create GTK window
        self.window = Gtk.ApplicationWindow(application=app)
        self.window.set_decorated(False)
        self.window.set_resizable(False)
        self.window.set_default_size(800, 28)

        # Create a label to show time, right aligned
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.set_hexpand(True)

        self.label_time = Gtk.Label()
        self.label_time.set_halign(Gtk.Align.END)
        box.append(self.label_time)

        self.window.set_child(box)

        # Tell layer shell this window is a top panel on all outputs
        self.layershell.set_layer(self.window, LayerShellV1.Layer.TOP)
        self.layershell.set_exclusive_zone(self.window, 28)
        self.layershell.set_keyboard_interactivity(self.window, False)
        self.layershell.set_anchor(self.window,
                                   left=True, right=True,
                                   top=True, bottom=False)

        self.window.show()

        # Update time every second
        GLib.timeout_add_seconds(1, self.update_time)
        self.update_time()

    def update_time(self):
        now = datetime.datetime.now()
        self.label_time.set_text(now.strftime("%a %H:%M:%S"))
        return True

    def run(self):
        self.app.run(None)

if __name__ == "__main__":
    topbar = TopBar()
    topbar.run()
