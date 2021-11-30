
cd /D "%~dp0\.."

pip3 install -r "%~dp0\requirements.txt"

python3 "%~dp0\main.py"

