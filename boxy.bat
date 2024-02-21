:: This batch file sets up the environment for the sandbox init process
:: It adds Scoop to the PATH and launches the rollout script.

REM Add Scoop to PATH for this session 
setx PATH "%PATH%;C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin" /M

REM Wait for 3 seconds
timeout /t 3

REM Check if Scoop is in the PATH
echo %PATH% | findstr /i /c:"C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin" > nul

IF %ERRORLEVEL% EQU 0 (
    REM Scoop is in the PATH, proceed with the rollout script
    powershell.exe -ExecutionPolicy Bypass -File "C:\Users\WDAGUtilityAccount\Desktop\scoop.ps1"
) ELSE (
    REM Scoop is not in the PATH, handle the error or take appropriate action
    echo Scoop is not in the PATH. Please check the installation.
)

REM Check if the previous command failed
IF %ERRORLEVEL% NEQ 0 (
    REM Previous command failed, try executing scoop.cmd instead
    powershell.exe -ExecutionPolicy Bypass -Command "try { & 'C:\Users\WDAGUtilityAccount\Desktop\scoop.cmd' } catch { Write-Host 'Failed to execute scoop.cmd' }"
)
