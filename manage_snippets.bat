@echo off
echo Snippet Management Utility
echo ========================
echo.
echo Choose an option:
echo 1. Add snippet interactively
echo 2. List all languages and snippet counts
echo 3. Add snippet via command line
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    python add_snippet.py
) else if "%choice%"=="2" (
    python add_snippet.py list
) else if "%choice%"=="3" (
    echo.
    echo Usage: python add_snippet.py <language> <snippet>
    echo Example: python add_snippet.py python "print('Hello')"
    echo.
    set /p language="Enter language: "
    set /p snippet="Enter snippet: "
    python add_snippet.py %language% "%snippet%"
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause 