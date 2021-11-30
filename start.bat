

pip install -r "%~dp0\requirements.txt"

IF "%1"=="" GOTO HAVE_0

:HAVE_1
        cd /D "%~dp1"
        goto RUN

:HAVE_0
        cd /D "%~dp0"
        goto RUN


:RUN
        python "%~dp0\main.py"

REM        pause

