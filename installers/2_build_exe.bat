@echo off
echo ===================================================
echo   Building Standalone Easypy Executable (.exe)
echo ===================================================
echo.
echo 1. Installing PyInstaller builder...
pip install pyinstaller

echo.
echo 2. Building easypy.exe (This may take a minute)...
cd ..
pyinstaller --noconfirm --onefile --console --name "easypy" --clean --hidden-import "rich" --hidden-import "requests" --hidden-import "pandas" --hidden-import "numpy" "launcher.py"

echo.
echo 3. Moving executable...
if not exist dist mkdir dist
move /Y dist\easypy.exe installers\easypy.exe
rmdir /s /q build
del /q easypy.spec

echo.
echo ===================================================
echo   BUILD COMPLETE!
echo ===================================================
echo Your standalone launcher is ready at:
echo   installers\easypy.exe
echo.
echo You can copy this file to any computer (even without Python)
echo and it will run your language!
pause
