@echo off
REM mines one-click launcher (compiles with MinGW g++)
setlocal
set MINGW=C:\Users\cheol\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin
set PATH=%MINGW%;%PATH%
cd /d %~dp0
if not exist mines.exe ( g++ -O2 -o mines.exe mines.cpp )
mines.exe %*
