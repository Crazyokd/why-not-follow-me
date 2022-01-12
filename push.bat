@echo off
:push 
git push origin main

if errorlevel 1 (
    goto :push
) else (
    echo Push Succeeded
)