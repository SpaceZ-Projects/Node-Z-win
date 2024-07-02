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
Python 3.8 or higher
Git

### Build App :

On Windows open PowerShell and run the following script:

```
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ezzygarmyz/nodez-win/main/scripts/build-win.ps1" -OutFile "$env:TEMP\build-win.ps1"; Invoke-Expression -Command "$env:TEMP\build-win.ps1"
```

### DEV Mode (Shell)
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
Clone the Repository:
```
git clone https://github.com/ezzygarmyz/nodez-win.git
cd nodez-win
```
Run the App
```
briefcase dev --update
```
