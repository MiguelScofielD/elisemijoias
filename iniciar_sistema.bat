@echo off
REM Ativa o ambiente virtual
cd /d D:\elisemijoias\  REM Caminho onde seu projeto está localizado

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Executa o servidor local Django
python manage.py runserver 0.0.0.0:8000
