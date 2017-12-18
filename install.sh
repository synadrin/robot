#!/bin/bash

# Dependencies
sudo apt-get update && sudo apt-get -y dist-upgrade
sudo apt-get -y install \
	bash-completion \
	git \
	vim \
	python3 \
	python3-pip \
	python3-pygame

# Python modules
sudo python3 -m pip install \
	pytmx \
	pyscroll

# Git project
sudo mkdir /usr/local/bin/robot
sudo chown pi:pi /usr/local/bin/robot
git clone https://github.com/synadrin/robot.git /usr/local/bin/robot

# Auto-login
cat /lib/systemd/system/getty@.service \
	| sed -e 's/ExecStart=-\/sbin\/agetty --noclear %I $TERM/ExecStart=-\/sbin\/agetty --noclear -a pi %I $TERM/;' \
	> /tmp/newgetty
sudo cp /tmp/newgetty /lib/systemd/system/getty@.service
rm /tmp/newgetty
