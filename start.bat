@echo off
set SCRIPT_DIR=%~dp0

echo Starting IIOT to Sink
echo =====================

if [%1]==["--clean"] goto purgevenv

echo|set /p="Checking environment..."
python --version >NUL  2>NUL
IF %ERRORLEVEL% NEQ 0 (
    echo FAIL!
    echo This tool requires Python3 and a venv for dependencies
    exit /b 1
)
if not exist "%SCRIPT_DIR%config.yml" (
    echo FAIL!
    echo config.yml not found! Review the readme to setup your environment
    exit /b 2
) 
echo OK
echo|set /p="Loading configuration."
if exist "%SCRIPT_DIR%config.yml" (
    python -m venv .
)
echo|set /p="."
call "%SCRIPT_DIR%Scripts\activate.bat"
echo .OK
echo|set /p="Loading dependencies..."

"%SCRIPT_DIR%Scripts\pip" install -r "%SCRIPT_DIR%requirements.txt" --quiet
if %ERRORLEVEL% NEQ 0 (
    echo FAIL!
    echo "pip could not install requirements. Please try installing manually within the venv:"
    echo "bin/pip3 install -r requirements.txt"
    exit 3
)
echo OK

echo Starting main loop...
"%SCRIPT_DIR%Scripts/Python" "%SCRIPT_DIR%start.py"
exit /B 0

:purgevenv
    rmdir /s /q %SCRIPT_DIR%/Scripts
    rmdir /s /q %SCRIPT_DIR%/Lib
    rmdir /s /q %SCRIPT_DIR%/Include
    del /f /q pyvenv.cfg
    echo OK