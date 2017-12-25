#!/bin/bash

# Adapted from https://yingtongli.me/blog/2016/12/21/splash.html

localDir=$(dirname $(realpath "${0}"))

echo "Installing: pre-requisites"
apt-get install fbi

echo "Installing: splashscreen.service"
cp "${localDir}/splashscreen.service" \
	/etc/systemd/system/splashscreen.service
echo "Installing: splash.png"
cp "${localDir}/splash.png" /opt/splash.png

echo "Disabling: login prompt"
systemctl disable getty@tty1
