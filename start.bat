@echo off
call venv/Scripts/activate
set PYTHONPATH=PYTHONPATH;./;./vall_e_x
python main.py
pause