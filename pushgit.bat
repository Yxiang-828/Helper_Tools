@echo off
REM Auto-commit and push script with timestamp
REM Usage: pushgit.bat [optional commit message]

setlocal enabledelayedexpansion

REM Get current timestamp
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do set datetime=%%i
set timestamp=%datetime:~0,8%_%datetime:~8,6%

REM Set default commit message if none provided
if "%~1"=="" (
    set commit_msg="Auto commit %timestamp%"
) else (
    set commit_msg="%~1 %timestamp%"
)

echo ========================================
echo    Git Auto-Commit and Push
echo ========================================
echo Timestamp: %timestamp%
echo Commit message: !commit_msg!
echo.

REM Add all changes
echo Adding files...
git add .
if errorlevel 1 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

REM Check if there are changes to commit
git status --porcelain > nul
if errorlevel 1 (
    echo No changes to commit.
    goto :push
)

REM Commit changes
echo Committing changes...
git commit -m !commit_msg!
if errorlevel 1 (
    echo ERROR: Failed to commit changes
    pause
    exit /b 1
)

:push
REM Push to remote
echo Pushing to remote...
git push
if errorlevel 1 (
    echo ERROR: Failed to push to remote
    pause
    exit /b 1
)

echo.
echo ========================================
echo          SUCCESS!
echo ========================================
echo All changes committed and pushed!
echo Timestamp: %timestamp%
echo.

REM Optional: Show last commit
echo Last commit:
git log --oneline -1

pause