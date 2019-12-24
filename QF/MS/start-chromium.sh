#!/bin/bash

#
# This file is auto-executed from here:
# /etc/xdg/lxsession/LXDE-pi/autostart
#
# you also need:
# xset s 0
# and
# xset -dpms
# in the file as well to prevent the screen from going to sleep

WEBSITE_URL="http://ms-roomcontroller.local:1880/timer/index.html"

set -e

CHROMIUM_TEMP=~/tmp/chromium
rm -Rf ~/.config/chromium/
rm -Rf "${CHROMIUM_TEMP}"
mkdir -p "${CHROMIUM_TEMP}"

chromium-browser \
        --disable \
        --disable-translate \
        --disable-infobars \
        --disable-suggestions-service \
        --disable-save-password-bubble \
        --disk-cache-dir=${CHROMIUM_TEMP}/cache/ \
        --user-data-dir=${CHROMIUM_TEMP}/user_data/ \
        --start-maximized \
        --kiosk ${WEBSITE_URL} &
          