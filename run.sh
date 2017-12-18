#!/bin/bash

robotDir=$(dirname "${0}")
today=$(date '+%Y-%m-%d-%H%M')
logDir=/home/pi/log
logFile="${logDir}/robot.${today}.log"
logFileOwner=pi:pi

mkdir -p "${logDir}"
chown "${logFileOwner}" "${logDir}"
touch "${logFile}"
chown "${logFileOwner}" "${logFile}"

pushd "${robotDir}"
python3 "${robotDir}/robot.py" \
	>> "${logFile}" 2>&1
popd
