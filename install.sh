#!/bin/bash

# Dependencies
sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install
	bash-completion \
	git \
	vim \
	python3 \
	python3-pip \
	openssh-server \
	xorg

# Python modules
python3 -m pip install --user \
	pygame \
	pytmx \
	pyscroll

# Git project
sudo mkdir /usr/local/bin/robot
sudo chown pi:pi /usr/local/bin/robot
git clone https://github.com/synadrin/robot.git /usr/local/bin/robot

# Xorg
echo "pgrep 'tmux|startx' || startx" >> ~/.profile
cat <<-EOF > ~/.xinitrc
	#!/bin/sh
	exec /usr/local/bin/robot/run.sh
EOF

# Auto-login
cat /lib/systemd/system/getty@.service \
	| sed -e 's/ExecStart=-\/sbin\/agetty --noclear %I $TERM/ExecStart=-\/sbin\/agetty --noclear -a pi %I $TERM/;' \
	> /tmp/newgetty
sudo cp /tmp/newgetty /lib/systemd/system/getty@.service
rm /tmp/newgetty
