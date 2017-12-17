#!/bin/bash

robotDir=$(dirname "${0}")
today=$(date '+%Y-%m-%d-%H%M')
pushd "${robotDir}"
python3 "${robotDir}/robot.py" \
	> ~/robot."${today}.log" 2>&1
popd
