```bat
@echo off
echo ================================
echo Creating Python virtual environment...
echo ================================

python -m venv SimVenv

echo.
echo Activating environment and installing dependencies...
call SimVenv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ================================
echo Environment ready!
echo Starting simulation...
echo ================================

python main.py

pause