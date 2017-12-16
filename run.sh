#!/bin/bash

robotDir=$(dirname "${0}")
pushd "${robotDir}"
python3 "${robotDir}/robot.py"
popd
