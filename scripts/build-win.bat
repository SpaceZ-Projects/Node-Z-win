@echo off
setlocal

set "repoUrl=https://github.com/SpaceZ-Projects/Node-Z-win.git"
set "localRepoPath=%USERPROFILE%\Desktop\nodez-win"
set "gitInstallerUrl=https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe"
set "pythonInstallerUrl=https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
set "gitInstallerPath=%TEMP%\Git-Installer.exe"
set "pythonInstallerPath=%TEMP%\Python-Installer.exe"

where git >nul 2>&1
if errorlevel 1 (
    call :InstallGit
)

git --version

where python >nul 2>&1
if errorlevel 1 (
    call :InstallPython
)

python --version


if not exist "%localRepoPath%" (
    git clone %repoUrl% %localRepoPath%
)


cd /d "%localRepoPath%"


where python >nul 2>&1
if errorlevel 1 (
    echo Python installation failed. Please install Python manually and try again.
    exit /b 1
)


python -m venv env
if not exist "env\Scripts\activate.bat" (
    echo Failed to find activate.bat script. Please make sure the virtual environment is created successfully.
    exit /b 1
)

call "env\Scripts\activate.bat"


pip install briefcase
briefcase package windows -p zip

call "env\Scripts\deactivate.bat"

echo Application packaged successfully.
endlocal
exit /b 1


:InstallGit
echo Git is not installed. Installing Git...
powershell -Command "Invoke-WebRequest -Uri '%gitInstallerUrl%' -OutFile '%gitInstallerPath%'"
start /wait "" "%gitInstallerPath%" /VERYSILENT /NORESTART
del /f "%gitInstallerPath%"
goto :eof


:InstallPython
echo Python is not installed. Installing Python...
powershell -Command "Invoke-WebRequest -Uri '%pythonInstallerUrl%' -OutFile '%pythonInstallerPath%'"
start /wait "" "%pythonInstallerPath%" /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=1
del /f "%pythonInstallerPath%"
goto :eof
