@echo off
REM Git Push Script - Automatically commit and push all changes
REM Usage: gitpush.bat

echo ========================================
echo         Git Auto Push
echo ========================================
echo.

REM Check if we're in a git repository
if not exist ".git" (
    echo ERROR: Not a git repository!
    echo Please run this from the root of your git repository.
    pause
    exit /b 1
)

echo Checking git status...
git status --porcelain >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git status failed. Make sure git is installed.
    pause
    exit /b 1
)

REM Check if there are any changes
for /f %%i in ('git status --porcelain 2^>nul') do set HAS_CHANGES=1

if not defined HAS_CHANGES (
    echo No changes to commit.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 0
)

echo.
echo Changes detected. Adding all files...
git add .

echo.
echo Creating commit...
git commit -m "Auto-commit: %date% %time%"

if %errorlevel% neq 0 (
    echo ERROR: Commit failed. You may need to resolve conflicts or set up git user info.
    echo.
    echo Try running:
    echo git config --global user.name "Your Name"
    echo git config --global user.email "your.email@example.com"
    echo.
    pause
    exit /b 1
)

echo.
echo Pushing to remote repository...
git push

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo           SUCCESS!
    echo ========================================
    echo.
    echo All changes have been committed and pushed!
    echo.
) else (
    echo.
    echo ========================================
    echo           PUSH FAILED
    echo ========================================
    echo.
    echo Commit was created locally but push failed.
    echo You may need to set up a remote repository or check your permissions.
    echo.
    echo To push manually later, run: git push
    echo.
)

echo Press any key to exit...
pause >nul