#!/bin/sh

# küçük bir log (test için)
LOG=/tmp/etahta-osk-wrapper.log
echo "wrapper started $(date)" >> "$LOG"

# 1. DBus hazır mı?
i=0
while ! dbus-send --session --dest=org.freedesktop.DBus \
        /org/freedesktop/DBus org.freedesktop.DBus.ListNames \
        >/dev/null 2>&1
do
    sleep 1
    i=$((i+1))
    [ "$i" -ge 30 ] && exit 0
done

echo "dbus ready $(date)" >> "$LOG"

# 2. Cinnamon session var mı?
i=0
while ! pgrep -u "$USER" cinnamon >/dev/null 2>&1
do
    sleep 1
    i=$((i+1))
    [ "$i" -ge 30 ] && exit 0
done

echo "cinnamon ready $(date)" >> "$LOG"

# 3. X ekranı hazır mı?
i=0
while ! xset q >/dev/null 2>&1
do
    sleep 1
    i=$((i+1))
    [ "$i" -ge 30 ] && exit 0
done

echo "X ready $(date)" >> "$LOG"

# her şey hazır → asıl script
/usr/lib/etahta/chrome-osk.py &

echo "chrome-osk started $(date)" >> "$LOG"
exit 0

