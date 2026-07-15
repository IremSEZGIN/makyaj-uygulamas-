@echo off
echo Sunucu baslatiliyor (Port 5009)...
uvicorn server:app --host 0.0.0.0 --port 5009
pause
