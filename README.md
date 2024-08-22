Node-Z (Windows)
======

## About the Project :

Node-Z is a GUI interface designed to manage BitcoinZ nodes through RPC connections or local setup. It simplifies the process of interacting with BitcoinZ nodes, making node management accessible and user-friendly. Key features include:

- Easy setup and configuration of local BitcoinZ nodes.
- Remote management of BitcoinZ nodes via RPC.
- Real-time monitoring and status updates.
- User-friendly interface for node operations.

## Screenshots :
- Main Wizard :
<p align="center"><img src="https://github.com/SpaceZ-Projects/Node-Z-win/blob/main/screenshot/main_wizard.png" </p>

- Main Menu :
<p align="center"><img src="https://github.com/SpaceZ-Projects/Node-Z-win/blob/main/screenshot/main_menu.png" </p>

- Cash Out :
<p align="center"><img src="https://github.com/SpaceZ-Projects/Node-Z-win/blob/main/screenshot/cash_out.png" </p>

- Wallet Manage :
<p align="center"><img src="https://github.com/SpaceZ-Projects/Node-Z-win/blob/main/screenshot/wallet_manage.png" </p>

- Insight Explorer :
<p align="center"><img src="https://github.com/SpaceZ-Projects/Node-Z-win/blob/main/screenshot/insight_explorer.png" </p>

- Mining Tools :
<p align="center"><img src="https://github.com/SpaceZ-Projects/Node-Z-win/blob/main/screenshot/mining_tools.png" </p>

- Briefcase: https://briefcase.readthedocs.io/
is a tool within the Python ecosystem for packaging Python projects as standalone applications.
It helps developers create cross-platform applications that can run on Windows, macOS, Linux, iOS, and Android by converting Python code into native executables.

- Toga: https://toga.readthedocs.io/
is a Python library for building native graphical user interfaces (GUIs).
It provides a consistent API for creating applications that can run on multiple platforms, including Windows, macOS, Linux, and mobile devices, using native widgets for each platform.

## Getting Started :

### Requirements :

- Python 3.8 or higher
- Git

### DEV Mode (Shell)
Clone the Repository:
```
git clone https://github.com/SpaceZ-Projects/Node-Z-win.git
cd Node-Z-win
```
Create a virtual environment :
```
python -m venv env
```
Run the following command to temporarily bypass the execution policy:
```
Set-ExecutionPolicy Bypass -Scope Process
```
Activate virtual environment:
```
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
After completing your tasks in the virtual environment, you can revert the execution policy to its previous state for security:
```
Set-ExecutionPolicy Restricted -Scope Process
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
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/SpaceZ-Projects/Node-Z-win/main/scripts/build-win.ps1" -OutFile "$env:TEMP\build-win.ps1"; Invoke-Expression -Command "$env:TEMP\build-win.ps1"
```
