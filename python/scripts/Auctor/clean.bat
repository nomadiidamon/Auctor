@echo off
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 "%~dp0..\..\tools\Auctor\clean.py" %*
) else (
    python "%~dp0..\..\tools\Auctor\clean.py" %*
)
set rc=%errorlevel%
pause
exit /b %rc%
