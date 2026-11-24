@echo off
cd /d C:\xampp\htdocs\pbcc
start "PBCC" C:\xampp\php\php.exe artisan serve --host=0.0.0.0 --port=8000
timeout /t 8 /nobreak >nul
start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "http://192.168.100.10:8000/opac"
