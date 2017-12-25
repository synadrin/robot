#!/bin/bash

# Adapted from https://yingtongli.me/blog/2016/12/21/splash.html

localDir=$(dirname $(realpath "${0}"))

cp "${localDir}/splashscreen.service" \
	/etc/systemd/system/splashscreen.service
cp "${localDir}/splash.png" /opt/splash.png
