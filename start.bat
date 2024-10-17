@echo off
set SCRIPT_DIR=%~dp0

setlocal
CALL :getparent PARENT
IF /I "%PARENT%" == "powershell" GOTO :ispowershell
IF /I "%PARENT%" == "pwsh" GOTO :ispowershell
endlocal
echo This script can only be run from PowerShell!
exit /b 3

:ispowershell
echo.
echo Starting IIOT to Sink
echo =====================

if [%1]==[--clean] goto purgevenv

:dostart
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
    copy "%SCRIPT_DIR%.gitignore" "%SCRIPT_DIR%gitignore.bak" >NUL  2>NUL
    python -m venv %SCRIPT_DIR%
    move /y "%SCRIPT_DIR%gitignore.bak" "%SCRIPT_DIR%.gitignore" >NUL  2>NUL
)
echo|set /p="."
call "%SCRIPT_DIR%Scripts\activate.bat"
echo .OK
echo|set /p="Loading dependencies..."

"%SCRIPT_DIR%Scripts\pip" install -r "%SCRIPT_DIR%requirements.txt" --quiet --disable-pip-version-check
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
    echo|set /p="Cleaning virtual environment..."
    rmdir /s /q %SCRIPT_DIR%/Scripts >NUL  2>NUL
    rmdir /s /q %SCRIPT_DIR%/Lib >NUL  2>NUL
    rmdir /s /q %SCRIPT_DIR%/Include >NUL  2>NUL
    del /f /q pyvenv.cfg >NUL  2>NUL
    echo OK
    goto dostart

:getparent
    SET "PSCMD=$ppid=$pid;while($i++ -lt 3 -and ($ppid=(Get-CimInstance Win32_Process -Filter ('ProcessID='+$ppid)).ParentProcessId)) {}; (Get-Process -EA Ignore -ID $ppid).Name"
    for /f "tokens=*" %%i in ('powershell -noprofile -command "%PSCMD%"') do SET %1=%%i