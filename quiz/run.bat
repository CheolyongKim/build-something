@echo off
REM quiz one-click launcher (GNU target; MSVC link.exe not installed on this box)
setlocal
set MINGW=C:\Users\cheol\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin
set PATH=%MINGW%;%PATH%
cd /d %~dp0
if not exist target\x86_64-pc-windows-gnu\release\quiz.exe (
  cargo build --target x86_64-pc-windows-gnu --release
)
target\x86_64-pc-windows-gnu\release\quiz.exe %*
