#!/bin/bash
# Detach the Python app from any terminal session so WSLg treats it
# as a standalone window (not associated with the terminal process group).

APPDIR="$(cd "$(dirname "$0")" && pwd)"

export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/1000
export QT_QPA_PLATFORM=wayland

# setsid: new session → no controlling terminal → WSLg shows it independently
setsid "$APPDIR/ow/bin/python" "$APPDIR/main.py" \
    > /tmp/atp-timer.log 2>&1 &

echo "ATP Timer launched (pid $!), log: /tmp/atp-timer.log"
