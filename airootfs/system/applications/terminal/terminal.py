import gi
import os
import pty
import subprocess
import termios

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk

def on_activate(app):
    window = Gtk.Window(application=app)
    window.set_default_size(800, 600)
    window.set_title("Terminal")

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    window.set_child(vbox)

    textview = Gtk.TextView()
    textview.set_editable(False)
    textview.set_cursor_visible(False)
    textview.set_hexpand(True)
    textview.set_vexpand(True)
    vbox.append(textview)
    buffer = textview.get_buffer()

    entry = Gtk.Entry()
    entry.set_placeholder_text("Type your command here")
    vbox.append(entry)

    # Setup PTY
    master_fd, slave_fd = pty.openpty()

    # Enable signal handling (Ctrl+C etc) on slave fd
    attrs = termios.tcgetattr(slave_fd)
    attrs[3] |= termios.ISIG
    termios.tcsetattr(slave_fd, termios.TCSANOW, attrs)

    process = subprocess.Popen(
        ["/bin/bash"],
        preexec_fn=os.setsid,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        text=True,
        bufsize=0,
        universal_newlines=True,
    )
    os.close(slave_fd)

    def append_text(text):
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, text)
        textview.scroll_to_iter(buffer.get_end_iter(), 0.0, True, 0.0, 1.0)

    def on_pty_data(source, condition):
        if condition == GLib.IO_IN:
            try:
                data = os.read(source, 1024).decode()
            except OSError:
                return False
            GLib.idle_add(append_text, data)
            return True
        return False

    GLib.io_add_watch(master_fd, GLib.IO_IN, on_pty_data)

    def on_entry_activate(entry):
        text = entry.get_text()
        if text:
            os.write(master_fd, (text + "\n").encode())
            entry.set_text("")

    entry.connect("activate", on_entry_activate)

    def on_key_press(controller, keyval, keycode, state):
        ctrl = state & Gdk.ModifierType.CONTROL_MASK
        if ctrl and keyval == Gdk.KEY_c:
            os.write(master_fd, b'\x03')
            return True
        return False

    # Connect key-press on entry or window (you can choose)
    key_controller = Gtk.EventControllerKey()
    key_controller.connect("key-pressed", on_key_press)
    entry.add_controller(key_controller)

    # or to capture globally, uncomment next line:
    # window.connect("key-press-event", on_key_press)

    window.present()

app = Gtk.Application(application_id='com.drawsko.terminal')
app.connect('activate', on_activate)
app.run(None)
