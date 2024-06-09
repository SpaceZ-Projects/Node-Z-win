import asyncio
import os
import subprocess
import json

from toga import App

class ClientCommands():
    def __init__(self, app:App):
        super().__init__()
        self.app = app
        data_path = self.app.paths.data
        self.bitcoinzd_file = os.path.join(data_path, "bitcoinz-cli.exe")
        
    
    async def _run_command(self, command):
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                if stdout:
                    data = json.loads(stdout.decode())
                    result = json.dumps(data, indent=4)
                    return result
            else:
                error_message = stderr.decode()
                print(f"Command {command[1]} failed with error: {error_message}")
                return None
        except Exception as e:
            print(f"An error occurred while running command {command[1]}: {e}")
            return None    
        
    
    async def getInfo(self):
        command = [self.bitcoinzd_file, "getinfo"]
        return await self._run_command(command)
    
                  
    async def z_getTotalBalance(self):
        command = [self.bitcoinzd_file, "z_gettotalbalance"]
        return await self._run_command(command)
    
    
    async def z_getBalance(self, address):
        command = [self.bitcoinzd_file, f"z_getbalance {address}"]
        return await self._run_command(command)
    
    
    async def getBlockchainInfo(self):
        command = [self.bitcoinzd_file, "getblockchaininfo"]
        return await self._run_command(command)
    
    
    async def getNetworkSolps(self):
        command = [self.bitcoinzd_file, "getnetworksolps"]
        return await self._run_command(command)
    
    
    async def getBestblockhash(self):
        command = [self.bitcoinzd_file, "getbestblockhash"]
        return await self._run_command(command)
    
    
    async def getUnconfirmedBalance(self):
        command = [self.bitcoinzd_file, "getunconfirmedbalance"]
        return await self._run_command(command)
    
    
    async def getDeprecationInfo(self):
        command = [self.bitcoinzd_file, "getdeprecationinfo"]
        return await self._run_command(command)
    
    
    async def getMempoolinfo(self):
        command = [self.bitcoinzd_file, "getmempoolinfo"]
        return await self._run_command(command)
    
    
    async def verifyChain(self):
        command = [self.bitcoinzd_file, "verifychain"]
        return await self._run_command(command)
    
    
    async def validateAddress(self, address):
        command = [self.bitcoinzd_file, f"validateaddress {address}"]
        return await self._run_command(command)
    
    
    async def z_validateAddress(self, address):
        command = [self.bitcoinzd_file, f"z_validateaddress {address}"]
        return await self._run_command(command)
    
    
    async def listTransactions(self):
        command = [self.bitcoinzd_file, f"listtransactions * 10"]
        return await self._run_command(command)
    
    
    async def getTransaction(self, txid):
        command = [self.bitcoinzd_file, f"gettransaction {txid}"]
        return await self._run_command(command)