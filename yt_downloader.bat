@echo off
if not exist "venv\" (
    python -m venv venv
    call venv\Scripts\activate
    pip install --upgrade -r requirements.txt
) else (
    call venv\Scripts\activate
)

python yt_downloader.py
pause