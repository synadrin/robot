#!/bin/bash

localDir=$(dirname $(realpath "${0}"))

echo "Installing: robot-game.service"
cp "${localDir}/robot-game.service" \
	/etc/systemd/system/robot-game.service

echo "Enabling: robot-game.service"
systemctl enable robot-game.service
