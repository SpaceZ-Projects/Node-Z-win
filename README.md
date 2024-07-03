Node-Z (Windows)
======

## About the Project :

Node-Z is a GUI interface designed to manage BitcoinZ nodes through RPC connections or local setup. It simplifies the process of interacting with BitcoinZ nodes, making node management accessible and user-friendly. Key features include:

- Easy setup and configuration of local BitcoinZ nodes.
- Remote management of BitcoinZ nodes via RPC.
- Real-time monitoring and status updates.
- User-friendly interface for node operations.

<p align="center"><img src="https://github.com/ezzygarmyz/nodez-win/blob/main/screenshot/nodez_screenshot.png" </p>

## Getting Started :

### Requirements :

- Python 3.8 or higher
- Git

### DEV Mode (Shell)
Clone the Repository:
```
git clone https://github.com/ezzygarmyz/nodez-win.git
cd nodez-win
```
Create and activate a virtual environment :
```
python -m venv env
env\Scripts\activate
```
Install BeeWare tools :
```
pip install briefcase
```
Install Requirements Packages :
```
pip install -U -r requirements.txt
```
Run the App
```
briefcase dev --update
```

### Build App :

```
briefcase build --update
```
Package (default):

Briefcase uses the WiX Toolset to build an MSI installer for a Windows App. WiX, in turn, requires that .NET Framework 3.5 is enabled

Wix MSI installer :
```
briefcase package windows -p msi
```

ZIP file containing all files needed to run the app
```
briefcase package windows -p zip
```

Package (Visual Studio):

Briefcase supports creating a full Visual Studio project for a Windows App. 
When you install Visual Studio, there are many optional components. You should ensure that you have installed the following:

- .NET Desktop Development - All default packages
- Desktop Development with C++ - All default packages - C++/CLI support for v143 build tools

Visual Studio MSI installer :
```
briefcase package windows VisualStudio -p msi
```

ZIP file :
```
briefcase package windows VisualStudio -p zip
```


Script :

Open PowerShell and run the following script:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ezzygarmyz/nodez-win/main/scripts/build-win.ps1" -OutFile "$env:TEMP\build-win.ps1"; Invoke-Expression -Command "$env:TEMP\build-win.ps1"
```
