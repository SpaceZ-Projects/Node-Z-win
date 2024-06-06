$repoUrl = "https://github.com/ezzygarmyz/nodez-win.git"
$localRepoPath = "$env:USERPROFILE\Desktop\nodez-win"

function Install-Git {
    Write-Host "Git is not installed. Installing Git..."
    $gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe"
    $gitInstallerPath = "$env:TEMP\Git-Installer.exe"
    Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $gitInstallerPath

    Start-Process -FilePath $gitInstallerPath -ArgumentList "/VERYSILENT /NORESTART" -Wait
    Remove-Item $gitInstallerPath -Force
}

function Install-Python {
    Write-Host "Python is not installed. Installing Python..."
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
    $pythonInstallerPath = "$env:TEMP\Python-Installer.exe"
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath

    Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_launcher=1" -Wait
    Remove-Item $pythonInstallerPath -Force
}

$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Install-Git
}

$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Install-Python
}

if (-not (Test-Path -Path $localRepoPath)) {
    git clone $repoUrl $localRepoPath
}

Set-Location -Path $localRepoPath

if (-not $pythonInstalled) {
    Write-Error "Python installation failed. Please install Python manually and try again."
    exit
}

python -m venv env

$activateScript = Join-Path $localRepoPath "env\Scripts\Activate.ps1"
if (-not (Test-Path -Path $activateScript)) {
    Write-Error "Failed to find Activate.ps1 script. Please make sure the virtual environment is created successfully."
    exit
}

& $activateScript

pip install briefcase

briefcase package windows -p zip

Write-Output "Application packaged successfully."
