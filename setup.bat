call python --version
rmdir /S /Q venv
call python -m venv venv
call venv\Scripts\activate.bat
call pip install -r requirements.txt
pause
