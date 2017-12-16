#!/bin/bash

robotDir=$(basedir "${0}")
pushd "${robotDir}"
python3 "${robotDir}/robot.py"
popd
