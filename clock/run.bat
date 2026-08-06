@echo off
REM clock one-click launcher (compiles with javac if needed)
setlocal
cd /d %~dp0
if not exist Clock.class ( javac Clock.java )
java Clock %*
