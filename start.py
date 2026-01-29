import os
import subprocess
import time
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pythonw = os.path.join(BASE_DIR, "venv", "Scripts", "pythonw.exe")
manage = os.path.join(BASE_DIR, "manage.py")

log_path = os.path.join(BASE_DIR, "run.log")

with open(log_path, "a") as log:
    subprocess.Popen(
        [pythonw, manage, "runserver", "127.0.0.1:8000"],
        cwd=BASE_DIR,
        stdout=log,
        stderr=log
    )

time.sleep(4)
webbrowser.open("http://127.0.0.1:8000")

