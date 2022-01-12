@echo off

@REM exit virtual environment
call .venv\Scripts\deactivate.bat > nul 2>&1

@REM delete ignore file
setlocal enabledelayedexpansion
for /f "eol=# delims=" %%i in (.gitignore) do (
    if exist %%i (
        set t=%%i
        @REM directory
        cd !t! > NUL 2>&1 && cd .. && RD /S /Q "!t!"
        del /S /Q !t! > NUL 2>&1
    )
)
endlocal