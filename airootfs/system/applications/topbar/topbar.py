from ctypes import CDLL
CDLL('libgtk4-layer-shell.so')

import gi
import time
import subprocess

gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')

from gi.repository import Gtk, GLib
from gi.repository import Gtk4LayerShell as LayerShell

def on_activate(app):
    window = Gtk.Window(application=app)
    window.set_default_size(0, 30)
    
    provider = Gtk.CssProvider()
    provider.load_from_path("gui.css")
    Gtk.StyleContext.add_provider_for_display(
        window.get_display(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    LayerShell.init_for_window(window)
    LayerShell.set_layer(window, LayerShell.Layer.TOP)
    LayerShell.set_anchor(window, LayerShell.Edge.TOP, True)
    LayerShell.set_anchor(window, LayerShell.Edge.LEFT, True)
    LayerShell.set_anchor(window, LayerShell.Edge.RIGHT, True)
    LayerShell.set_margin(window, LayerShell.Edge.TOP, 0)
    LayerShell.set_margin(window, LayerShell.Edge.LEFT, 0)
    LayerShell.set_margin(window, LayerShell.Edge.RIGHT, 0)
    LayerShell.auto_exclusive_zone_enable(window)

    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    window.set_child(box)

    menu_button = Gtk.MenuButton()
    menu_button.get_style_context().add_class("flat")
    menu_button.set_size_request(-1, 30)
    menu_button.set_label("DRAWSKO")

    popover = Gtk.Popover()
    menu_button.set_popover(popover)

    popover_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
    popover_box.set_margin_start(10)
    popover_box.set_margin_end(10)
    popover_box.set_margin_top(10)
    popover_box.set_margin_bottom(10)
    popover.set_child(popover_box)

    btn1 = Gtk.Button(label="About This Computer")
    btn2 = Gtk.Button(label="Terminal")
    btn3 = Gtk.Button(label="Restart")
    btn4 = Gtk.Button(label="Shutdown")

    def on_about_clicked(button):
        subprocess.Popen(["python3", "/system/applications/about/about.py"])

    btn1.connect("clicked", on_about_clicked)

    def on_terminal_clicked(button):
        subprocess.Popen(["python3", "/system/applications/terminal/terminal.py"])

    btn2.connect("clicked", on_terminal_clicked)

    popover_box.append(btn1)
    popover_box.append(btn2)
    popover_box.append(btn3)
    popover_box.append(btn4)

    box.append(menu_button)

    spacer = Gtk.Box()
    spacer.set_hexpand(True)
    box.append(spacer)

    clock_label = Gtk.Label()
    clock_label.set_margin_end(10)
    box.append(clock_label)

    def update_time():
        now = time.strftime("%H:%M:%S")
        clock_label.set_text(now)
        return True

    GLib.timeout_add_seconds(1, update_time)
    update_time()

    window.present()

app = Gtk.Application(application_id='com.drawsko.topbar')
app.connect('activate', on_activate)
app.run(None)
