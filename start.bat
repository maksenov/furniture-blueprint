
cd /D "%~dp0\.."

pip install -r "%~dp0\requirements.txt" 

python "%~dp0\main.py"

pause
