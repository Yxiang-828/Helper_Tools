@echo off
setlocal

:: ============================================================================
:: Title:   AMD GPU ROCm Setup for WSL
:: Author:  Gemini
:: Purpose: Automates the installation of ROCm and PyTorch for AI in WSL.
:: ============================================================================


:: --- 1. Administrative Rights Check ---
fltmc >nul 2>&1 || (
    echo =======================================================================
    echo  ERROR: Administrator permissions are required.
    echo =======================================================================
    echo.
    echo  Please right-click this script and select "Run as administrator".
    echo.
    pause
    exit /b 1
)


:: --- 2. Display Header and Introduction ---
cls
echo =======================================================================
echo          AMD GPU ROCm Setup for WSL (AI Acceleration)
echo =======================================================================
echo.
echo  This script will automate the following tasks inside your WSL Ubuntu:
echo    1. Install ROCm drivers and libraries for your AMD GPU.
echo    2. Add your user to the required 'render' and 'video' groups.
echo    3. Install PyTorch with ROCm support for GPU-accelerated AI.
echo    4. Install OpenAI Whisper as a sample AI application.
echo.
echo  Prerequisites:
echo    - Windows 11
echo    - WSL2 with an Ubuntu distribution installed.
echo    - An AMD GPU that supports ROCm.
echo.
echo =======================================================================
echo  Press any key to begin the setup...
pause >nul


:: --- 3. Check for WSL Installation ---
echo.
echo [*] Checking for WSL installation...
wsl --status >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: WSL is not installed or not enabled.
    echo     Please install it from the Microsoft Store or by running 'wsl --install'.
    pause
    exit /b 1
)
echo [+] WSL is installed.


:: --- 4. Check for an Ubuntu Distribution ---
echo [*] Checking for an Ubuntu distribution in WSL...
wsl -l -q | findstr /i "Ubuntu" >nul
if %errorlevel% neq 0 (
    echo [!] ERROR: No 'Ubuntu' distribution found in WSL.
    echo     Please install Ubuntu from the Microsoft Store first.
    pause
    exit /b 1
)
echo [+] Ubuntu distribution found.


:: --- 5. Generate the Linux Shell Script ---
echo [*] Preparing setup script for execution inside WSL...
(
    echo #!/bin/bash
    echo # This script is auto-generated and runs inside WSL.
    echo set -e
    echo.
    echo "--- [1/6] Updating package lists ---"
    echo "This requires your WSL password."
    echo.
    echo sudo apt-get update -y
    echo sudo apt-get upgrade -y
    echo.
    echo "--- [2/6] Installing prerequisites ---"
    echo sudo apt-get install -y wget gpg
    echo.
    echo "--- [3/6] Adding AMD ROCm repository ---"
    echo "Downloading and adding AMD's official GPG key..."
    echo "wget -qO - https://repo.radeon.com/rocm/rocm.gpg.key ^| sudo gpg --dearmor -o /usr/share/keyrings/rocm.gpg"
    echo "Adding the repository to your sources list..."
    echo "echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.0/ ubuntu main' ^| sudo tee /etc/apt/sources.list.d/rocm.list"
    echo sudo apt-get update -y
    echo.
    echo "--- [4/6] Installing ROCm and adding user to groups ---"
    echo "Installing core ROCm packages (this may take several minutes)..."
    echo sudo apt-get install -y rocm-hip-sdk rocm-dev
    echo.
    echo "Adding current user (\$LOGNAME) to 'render' and 'video' groups..."
    echo sudo usermod -a -G render,video \$LOGNAME
    echo.
    echo "--- [5/6] Installing PyTorch with ROCm and Whisper ---"
    echo "Installing Python and Pip..."
    echo sudo apt-get install -y python3-pip
    echo "Installing PyTorch for ROCm..."
    echo pip3 install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
    echo "Installing OpenAI Whisper..."
    echo pip3 install --upgrade openai-whisper
    echo.
    echo "--- [6/6] Verifying PyTorch and ROCm Installation ---"
    echo "python3 -c 'import torch; print(\"PyTorch version:\", torch.__version__); print(\"ROCm available:\", torch.cuda.is_available()); print(\"Device name:\", torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\")'"
    echo.
) > wsl_rocm_setup.sh


:: --- 6. Execute the Script in WSL ---
echo.
echo =======================================================================
echo          Starting the main setup process inside WSL
echo =======================================================================
echo.
echo  The script will now run inside your Ubuntu WSL distribution.
echo.
echo  >>> IMPORTANT: You will be prompted to enter your SUDO password for Ubuntu. <<<
echo.
echo  This process can take 10-30 minutes. Please be patient.
echo.
pause

wsl -d Ubuntu -- bash wsl_rocm_setup.sh

if %errorlevel% neq 0 (
    echo.
    echo =======================================================================
    echo  [!] ERROR: The WSL setup script failed.
    echo =======================================================================
    echo.
    echo  Please check the output above for any error messages.
    echo  Common issues include incorrect passwords, network problems, or
    echo  an unsupported GPU.
    del wsl_rocm_setup.sh >nul 2>&1
    pause
    exit /b 1
)


:: --- 7. Cleanup and Final Instructions ---
del wsl_rocm_setup.sh
cls
echo.
echo =======================================================================
echo                    ✅ Setup Completed Successfully! ✅
echo =======================================================================
echo.
echo  ROCm and PyTorch have been installed in your WSL Ubuntu environment.
echo.
echo  --- IMPORTANT FINAL STEP ---
echo.
echo  You MUST restart your computer for all changes (especially user
echo  group permissions) to take full effect.
echo.
echo  After restarting, your AI applications running from Windows that support
echo  WSL acceleration will automatically detect and use your AMD GPU.
echo.
pause
exit /b 0