@echo off
cd /d "%~dp0"
git add -A
git commit -m "Valyxo v0.31 - Production Ready - Full-Stack Platform v0.31"
git log --oneline -1
echo.
echo Commit successful!
