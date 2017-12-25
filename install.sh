#!/bin/bash

LOCAL_USER=pi
LOCAL_GROUP=pi
localDir=$(dirname $(realpath "${0}"))
robotDir=/usr/local/bin/robot
OS=$(cat /etc/os-release)

function show_help()
{
	echo "Usage: ${0} <vm|rpi>"
	exit 3
}

function install_software()
{
	apt-get update && apt-get -y dist-upgrade

	case "${1}" in
		vm)
			apt-get -y install \
				bash-completion \
				git \
				vim \
				python3 \
				python3-pip
			;;
		rpi)
			apt-get -y install \
				git \
				python3 \
				python3-pip \
				python3-pygame
			;;
		*)
			;;
	esac
}

function install_services()
{
	"${robotDir}/splashscreen/install.sh"
	"${robotDir}/robot-game/install.sh"
}

function install_python_modules()
{
	python3 -m pip install pytmx pyscroll
}

function install_virtualbox_guest_additions()
{
	apt-get -y install build-essential module-assistant
	m-a prepare
	echo "####################"
	echo "# Insert the \"Guest Additions CD image\" and press enter when ready."
	echo "####################"
	read
	mount /media/cdrom
	sh /media/cdrom/VBoxLinuxAdditions.run
	umount /media/cdrom
	eject /media/cdrom
}

function clone_project()
{
	mkdir -p "${robotDir}" > /dev/null
	chown "${LOCAL_USER}:${LOCAL_GROUP}" "${robotDir}"
	sudo -u "${LOCAL_USER}" \
		git clone https://github.com/synadrin/robot.git \
		"${robotDir}"
}

case "${1}" in
	vm)
		install_software vm
		install_python_modules
		install_virtualbox_guest_additions
		clone_project
		install_services
		;;
	rpi)
		install_software rpi
		install_python_modules
		clone_project
		install_services
		;;
	*)
		show_help
		;;
esac
