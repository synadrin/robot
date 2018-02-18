@ECHO OFF

SET robotDir=%~dp0
SET robotDir=%robotDir:~0,-1%
SET logDir=%robotDir%\log
SET logFilename=%logDir%\robot.log

MKDIR "%logDir%" 2> nul

PUSHD "%robotDir%"
SET DISPLAY=Windows
py "%robotDir%\robot.py" >> "%logFilename%"
POPD
