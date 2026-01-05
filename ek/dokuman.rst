Chrome Odaklı Sanal Klavye (eta-keyboard / Onboard) – Python Servisi
==================================================================

Bu doküman, Chrome penceresi odaklandığında sanal klavyeyi
otomatik açan, odak kaybolduğunda kapatan Python tabanlı
hafif bir kullanıcı servisini anlatır.

Öncelik sırası:

1. **eta-keyboard (D-Bus)**
2. **Onboard (fallback)**

------------------------------------------------------------
1. Genel Mimari
------------------------------------------------------------

Servis kullanıcı oturumunda çalışır ve sürekli olarak
aktif pencereyi izler.

Davranış:

- Aktif pencere **Google Chrome** ise:
  - eta-keyboard varsa → ``show()``
  - yoksa → ``onboard`` başlatılır
- Chrome odaktan çıkarsa:
  - eta-keyboard → ``hide()``
  - onboard → kapatılır

------------------------------------------------------------
2. Kullanılan Teknolojiler
------------------------------------------------------------

- Python 3
- GObject Introspection
  - ``Wnck`` → pencere odak takibi
- D-Bus
  - ``org.eta.virtualkeyboard`` (opsiyonel)
- systemd --user

------------------------------------------------------------
3. eta-keyboard D-Bus Arayüzü
------------------------------------------------------------

Servis adı::

  org.eta.virtualkeyboard

Object path::

  /VirtualKeyboard

Temel metodlar::

  show(in b password)
  hide()
  toggle()
  showForce(in b password)

------------------------------------------------------------
4. Python Kodunun Mantığı
------------------------------------------------------------

Başlangıçta sistemde eta-keyboard olup olmadığı kontrol edilir.

Pseudo akış::

  Eğer D-Bus servisi mevcutsa:
      eta-keyboard kullan
  Aksi halde:
      onboard fallback

Odak değişimi şu şekilde izlenir::

  Aktif pencere değişti
      ↓
  Pencere başlığı Chrome mu?
      ↓
  Evet → klavyeyi aç
  Hayır → klavyeyi kapat

------------------------------------------------------------
5. Python Kodunun Tam Hali
------------------------------------------------------------

.. code-block:: python

    #!/usr/bin/env python3
    import gi
    gi.require_version("Wnck", "3.0")
    from gi.repository import Wnck, GLib

    import subprocess
    import dbus
    import time

    USE_ETA = False
    eta_iface = None
    onboard_proc = None

    def detect_eta_keyboard():
        global USE_ETA, eta_iface
        try:
            bus = dbus.SessionBus()
            obj = bus.get_object("org.eta.virtualkeyboard", "/VirtualKeyboard")
            eta_iface = dbus.Interface(obj, "org.eta.virtualkeyboard")
            USE_ETA = True
        except Exception:
            USE_ETA = False

    def show_keyboard():
        global onboard_proc
        if USE_ETA:
            eta_iface.show(False)
        else:
            if onboard_proc is None or onboard_proc.poll() is not None:
                onboard_proc = subprocess.Popen(["onboard"])

    def hide_keyboard():
        global onboard_proc
        if USE_ETA:
            eta_iface.hide()
        else:
            if onboard_proc and onboard_proc.poll() is None:
                onboard_proc.terminate()
                onboard_proc = None

    def check_focus():
        screen = Wnck.Screen.get_default()
        screen.force_update()

        win = screen.get_active_window()
        if not win:
            hide_keyboard()
            return True

        name = win.get_name().lower()
        wmclass = " ".join(win.get_class_group_name() or "").lower()

        if "chrome" in name or "chrome" in wmclass:
            show_keyboard()
        else:
            hide_keyboard()

        return True

    def main():
        detect_eta_keyboard()
        GLib.timeout_add(300, check_focus)
        loop = GLib.MainLoop()
        loop.run()

    if __name__ == "__main__":
        main()

------------------------------------------------------------
6. systemd --user Servisi
------------------------------------------------------------

Servis dosyası::

  ~/.config/systemd/user/eta-chrome-osk.service

İçerik::

  [Unit]
  Description=Chrome OSK Controller
  After=graphical-session.target

  [Service]
  ExecStart=/usr/bin/eta-chrome-osk
  Restart=always

  [Install]
  WantedBy=default.target

------------------------------------------------------------
7. Özellikler
------------------------------------------------------------

- xdotool kullanılmaz
- Çok hafif (poll + Wnck)
- X11 uyumlu
- eta-keyboard öncelikli
- Onboard fallback
- Paketlenebilir yapı

------------------------------------------------------------
8. Geliştirme Fikirleri
------------------------------------------------------------

- Wayland algılama
- Firefox için aynı mantık
- Dokunmatik cihaz kontrolü
- toggleAutoShow entegrasyonu
- AT-SPI olaylarıyla tetikleme

------------------------------------------------------------
9. Sonuç
------------------------------------------------------------

Bu yapı, Chrome’un X11 altında sanal klavye
tetiklememesini telafi eder ve
dokunmatik cihazlarda doğal bir kullanıcı deneyimi sağlar.

Dağıtım bağımsız, paketlenebilir ve
kurumsal imajlarda kullanılabilir.

