#!/usr/bin/env python3
import gi
import dbus

gi.require_version("Wnck", "3.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Wnck, Gtk

class ChromeKeyboardManager:
    def __init__(self):
        # D-Bus bağlantısı
        self.bus = dbus.SessionBus()
        self.kbd = self.bus.get_object(
            "org.eta.virtualkeyboard",
            "/VirtualKeyboard"
        )
        self.iface = dbus.Interface(
            self.kbd,
            "org.eta.virtualkeyboard"
        )

        # Window focus (olay tabanlı)
        self.screen = Wnck.Screen.get_default()
        self.screen.force_update()
        self.screen.connect(
            "active-window-changed",
            self.on_active_window_changed
        )

    def on_active_window_changed(self, screen, prev):
        win = screen.get_active_window()
        if not win:
            self.hide()
            return

        name = win.get_name()

        if "Google Chrome" in name:
            self.show_normal()
        else:
            self.hide()

    # ---- Klavye Kontrolleri ----

    def show_normal(self):
        try:
            self.iface.show(False)   # normal input
        except Exception:
            pass

    def show_password(self):
        try:
            self.iface.show(True)    # password modu
        except Exception:
            pass

    def hide(self):
        try:
            self.iface.hide()
        except Exception:
            pass


def main():
    ChromeKeyboardManager()
    Gtk.main()

if __name__ == "__main__":
    main()

