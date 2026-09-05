@echo off
setlocal
cd /d "%~dp0"

echo.
echo Launcher folder: %CD%
echo.

if exist "app.py" goto :found

echo app.py is not in this folder. Looking one level down...
for /d %%D in (*) do (
  if exist "%%D\app.py" (
    echo Found nested project: %CD%\%%D
    cd /d "%CD%\%%D"
    goto :found
  )
)

echo.
echo Could not find app.py next to this run.bat.
echo Open File Explorer, search for app.py, then run this script from THAT folder.
echo Do not use C:\Users\Admin\Downloads\flightops-assignment-cursor-skyvault-memory-238c
echo if app.py is not sitting in that exact directory.
echo.
dir /s /b app.py 2>nul
pause
exit /b 1

:found
echo Using project folder: %CD%
echo Files:
dir /b app.py memory.py tools.py 2>nul
echo.

if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" app.py
) else (
  py -3 app.py
)

echo.
pause
