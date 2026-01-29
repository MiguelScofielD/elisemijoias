@REM @echo off
@REM REM Ativa o ambiente virtual
@REM cd /d D:\elisemijoias REM Caminho onde seu projeto está localizado

@REM REM Ativa o ambiente virtual
@REM call venv\Scripts\activate

@REM start http://127.0.0.1:8000

@REM REM Executa o servidor local Django
@REM python manage.py runserver 127.0.0.1:8000


@echo off
cd /d D:\elisemijoias
venv\Scripts\pythonw.exe start.py
exit
