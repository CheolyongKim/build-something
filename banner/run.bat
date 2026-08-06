@echo off
REM banner one-click launcher (compiles with MinGW gcc)
setlocal
set MINGW=C:\Users\cheol\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin
set PATH=%MINGW%;%PATH%
cd /d %~dp0
if not exist banner.exe ( gcc -O2 -o banner.exe banner.c )
banner.exe %*
