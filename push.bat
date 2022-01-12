@echo off
:push_main
git push origin main

if errorlevel 1 (
    goto :push_main
)

:push_tag
git push origin --tags

if errorlevel 1 (
    goto :push_tag
) else (
    echo Push Succeeded
)