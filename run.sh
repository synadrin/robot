#!/bin/bash

robotDir=$(dirname $(realpath "${0}"))
today=$(date '+%Y-%m-%d-%H%M')
logDir=/home/pi/log
logFile="${logDir}/robot.${today}.log"
logFileOwner=pi:pi

mkdir -p "${logDir}" > /dev/null
chown "${logFileOwner}" "${logDir}"
touch "${logFile}"
chown "${logFileOwner}" "${logFile}"

pushd "${robotDir}" > /dev/null
/usr/bin/python3 "${robotDir}/robot.py" \
	>> "${logFile}" 2>&1
popd > /dev/null
