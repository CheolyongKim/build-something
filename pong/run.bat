@echo off
REM pong one-click launcher (compiles with MinGW gcc)
setlocal
set MINGW=C:\Users\cheol\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin
set PATH=%MINGW%;%PATH%
cd /d %~dp0
if not exist pong.exe ( gcc -O2 -o pong.exe pong.c )
pong.exe %*
