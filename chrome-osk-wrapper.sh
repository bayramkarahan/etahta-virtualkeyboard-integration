#!/bin/bash
# Dynamic X11 display for user session
export DISPLAY=${DISPLAY:-:0}
export XAUTHORITY=$HOME/.Xauthority

exec /usr/bin/python3 /usr/lib/etahta/chrome-osk.py

