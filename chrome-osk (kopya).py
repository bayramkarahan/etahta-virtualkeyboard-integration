#!/usr/bin/env python3
import gi
import subprocess
import os

gi.require_version("Wnck", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Wnck, Gtk

# ---- ETA keyboard (D-Bus) detection ----
USE_ETA = False
iface = None

try:
    import dbus
    bus = dbus.SessionBus()
    kbd = bus.get_object("org.eta.virtualkeyboard", "/VirtualKeyboard")
    iface = dbus.Interface(kbd, "org.eta.virtualkeyboard")
    USE_ETA = True
except Exception:
    USE_ETA = False

# ---- Helpers ----
def show_keyboard():
    if USE_ETA:
        try:
            iface.show(False)
        except Exception:
            pass
    else:
        subprocess.Popen(["onboard"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def hide_keyboard():
    if USE_ETA:
        try:
            iface.hide()
        except Exception:
            pass
    else:
        subprocess.Popen(["pkill", "-f", "onboard"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ---- Main manager ----
class BrowserKeyboardManager:
    def __init__(self):
        self.screen = Wnck.Screen.get_default()
        self.screen.force_update()
        self.screen.connect("active-window-changed", self.on_active_window_changed)

    def on_active_window_changed(self, screen, prev):
        win = screen.get_active_window()
        if not win:
            hide_keyboard()
            return

        app = win.get_application()
        if not app:
            hide_keyboard()
            return

        app_name = app.get_name().lower()

        # Chrome + Firefox
        if "chrome" in app_name or "firefox" in app_name:
            show_keyboard()
        else:
            hide_keyboard()

def main():
    BrowserKeyboardManager()
    Gtk.main()

if __name__ == "__main__":
    main()

