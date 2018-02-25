@ECHO OFF

SET robotDir=%~dp0
SET robotDir=%robotDir:~0,-1%
SET logDir=%robotDir%\log
SET logFilename=%logDir%\robot.log

MKDIR "%logDir%" 2> nul

ECHO [%DATE% %TIME%] -------- >> "%logFilename%"

PUSHD "%robotDir%"
SET DISPLAY=Windows
py "%robotDir%\robot.py" 1>> "%logFilename%" 2>&1
POPD
