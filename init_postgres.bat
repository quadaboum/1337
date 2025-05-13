@echo off
call venv\Scripts\activate
set DATABASE_URL=postgresql://remplace_moi
python init_db.py
pause
