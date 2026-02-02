@echo off
echo ===================================================
echo   Installing Easypy Globally (Local Dev Mode)
echo ===================================================
echo.
echo 1. Installing dependencies...
pip install -r ..\requirements.txt

echo.
echo 2. Installing package...
pip install -e ..

echo.
echo ===================================================
echo   SUCCESS!
echo ===================================================
echo You can now open a NEW terminal window and type:
echo.
echo   easypy --version
echo.
echo to use it anywhere on your system!
pause
