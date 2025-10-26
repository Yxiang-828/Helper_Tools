@echo off
REM Run Vivado batch synthesis script
REM Usage: run_viva.bat

echo Running Vivado synthesis script...
echo.

cd cmd_vivado

"C:\Xilinx\Vivado\2018.2\bin\vivado.bat" -mode batch -source full_script.tcl

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! bitstream gen completed.
) else (
    echo.
    echo ERROR: bitstream gen failed. Check the output above.
)
cd ..
echo.
pause
