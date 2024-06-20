import asyncio
import os
import subprocess
import json
import binascii

from toga import App, platform

class ClientCommands():
    def __init__(self, app:App):
        super().__init__()
        self.app = app
        data_path = self.app.paths.data
        self.bitcoinz_cli_file = os.path.join(data_path, "bitcoinz-cli.exe")
        
    
    async def _run_command(self, command):
        try:
            process = await asyncio.create_subprocess_shell(
                ' '.join(command),
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
        command = [self.bitcoinz_cli_file, "getinfo"]
        return await self._run_command(command)
    
                  
    async def z_getTotalBalance(self):
        command = [self.bitcoinz_cli_file, "z_gettotalbalance"]
        return await self._run_command(command)
    
    
    async def z_getBalance(self, address):
        command = [self.bitcoinz_cli_file, f'z_getbalance "{address}"']
        return await self._run_command(command)
    
    
    async def getBlockchainInfo(self):
        command = [self.bitcoinz_cli_file, "getblockchaininfo"]
        return await self._run_command(command)
    
    
    async def getNetworkSolps(self):
        command = [self.bitcoinz_cli_file, "getnetworksolps"]
        return await self._run_command(command)
    
    
    async def getBestblockhash(self):
        command = [self.bitcoinz_cli_file, "getbestblockhash"]
        return await self._run_command(command)
    
    
    async def getUnconfirmedBalance(self):
        command = [self.bitcoinz_cli_file, "getunconfirmedbalance"]
        return await self._run_command(command)
    
    
    async def getDeprecationInfo(self):
        command = [self.bitcoinz_cli_file, "getdeprecationinfo"]
        return await self._run_command(command)
    
    
    async def getMempoolinfo(self):
        command = [self.bitcoinz_cli_file, "getmempoolinfo"]
        return await self._run_command(command)
    
    
    async def verifyChain(self):
        command = [self.bitcoinz_cli_file, "verifychain"]
        return await self._run_command(command)
    
    
    async def listAddressgroupPings(self):
        command = [self.bitcoinz_cli_file, "listaddressgroupings"]
        return await self._run_command(command)
    
    
    async def z_listAddresses(self):
        command = [self.bitcoinz_cli_file, "z_listaddresses"]
        return await self._run_command(command)
    
    
    async def validateAddress(self, address):
        command = [self.bitcoinz_cli_file, f"validateaddress {address}"]
        return await self._run_command(command)
    
    
    async def z_validateAddress(self, address):
        command = [self.bitcoinz_cli_file, f"z_validateaddress {address}"]
        return await self._run_command(command)
    
    
    async def listTransactions(self):
        command = [self.bitcoinz_cli_file, f'listtransactions "*" 25']
        return await self._run_command(command)
    
    
    async def getTransaction(self, txid):
        command = [self.bitcoinz_cli_file, f"gettransaction {txid}"]
        return await self._run_command(command)
    
    
    async def sendToAddress(self, address, amount, comment):
        print(address, amount, comment)
        if comment:
            command = [self.bitcoinz_cli_file, f'sendtoaddress "{address}" {amount} "{comment}"']
        else:
            command = [self.bitcoinz_cli_file, f'sendtoaddress "{address}" {amount}']
        return await self._run_command(command)
    
    
    async def z_sendMany(self, uaddress, toaddress, amount, comment, txfee):
        if comment:
            hex_comment = binascii.hexlify(comment.encode()).decode()
            command = [
                self.bitcoinz_cli_file,
                f'z_sendmany "{uaddress}" \'[{{"address": "{toaddress}", "amount": {amount}, "memo": "{hex_comment}"}}]\'','1', txfee
            ]
            return await self._run_command(command)
        else:
            command = [
                self.bitcoinz_cli_file,
                f'z_sendmany "{uaddress}" \'[{{"address": "{toaddress}", "amount": {amount}}}]\'','1', txfee
            ]
            
    
    async def z_getOperationStatus(self, operation_ids):
        command = [
            self.bitcoinz_cli_file,
            f'z_getoperationstatus {operation_ids}'
        ]
        return await self._run_command(command)
    
    
    
    async def z_getOperationResult(self, operation_ids):
        command = [
            self.bitcoinz_cli_file,
            f'z_getoperationresult {operation_ids}'
        ]
        return await self._run_command(command)