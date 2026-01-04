#!/usr/bin/env python3
import gi
import subprocess

gi.require_version("Wnck", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Wnck, Gtk

# Try ETA virtual keyboard via D-Bus
USE_ETA = False
try:
    import dbus
    bus = dbus.SessionBus()
    kbd = bus.get_object("org.eta.virtualkeyboard", "/VirtualKeyboard")
    iface = dbus.Interface(kbd, "org.eta.virtualkeyboard")
    USE_ETA = True
except Exception:
    USE_ETA = False

class ChromeKeyboardManager:
    def __init__(self):
        self.screen = Wnck.Screen.get_default()
        self.screen.force_update()
        self.screen.connect("active-window-changed", self.on_active_window_changed)

    def on_active_window_changed(self, screen, prev):
        win = screen.get_active_window()
        if not win:
            self.hide()
            return

        name = win.get_name()
        if "Google Chrome" in name:
            self.show()
        else:
            self.hide()

    def show(self):
        if USE_ETA:
            try:
                iface.show(False)
            except Exception:
                pass
        else:
            subprocess.Popen(["onboard"])

    def hide(self):
        if USE_ETA:
            try:
                iface.hide()
            except Exception:
                pass
        else:
            subprocess.Popen(["pkill", "onboard"])

def main():
    ChromeKeyboardManager()
    Gtk.main()

if __name__ == "__main__":
    main()
