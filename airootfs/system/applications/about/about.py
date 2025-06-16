import gi
import systeminfo

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, GLib

def on_activate(app):
    window = Gtk.Window(application=app)
    window.set_default_size(300, 400)
    window.set_title("About Drawsko")
    window.set_resizable(False)
    
    provider = Gtk.CssProvider()
    provider.load_from_path("gui.css")
    Gtk.StyleContext.add_provider_for_display(
        window.get_display(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
    vbox.set_halign(Gtk.Align.CENTER)
    vbox.set_valign(Gtk.Align.CENTER)
    window.set_child(vbox)

    cpu_label = Gtk.Label(label=f"CPU: {systeminfo.get_cpu()}")
    ram_label = Gtk.Label(label=f"RAM: {systeminfo.get_ram()}")
    gpu_label = Gtk.Label(label=f"GPU: {systeminfo.get_gpu()}")
    gpu_label.set_wrap(True)
    os_label = Gtk.Label(label=f"OS: {systeminfo.get_os()}")

    for lbl in (cpu_label, ram_label, gpu_label, os_label):
        lbl.set_xalign(0.5)
        vbox.append(lbl)

    window.present()

app = Gtk.Application(application_id='com.drawsko.about')
app.connect('activate', on_activate)
app.run(None)
