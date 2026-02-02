@echo off
echo ===================================================
echo   Building Docker Image
echo ===================================================

echo 1. Building image 'easypy-engine'...
docker build -t easypy-engine ..

echo.
echo 2. Verifying build...
docker run --rm easypy-engine --version

echo.
echo ===================================================
echo   SUCCESS! 
echo   To perform actions:
echo   docker run -it easypy-engine run my_script.ep
echo ===================================================
pause
