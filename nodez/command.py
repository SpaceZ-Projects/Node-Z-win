import asyncio
import os
import subprocess
import json
import binascii

from toga import App

class ClientCommands():
    def __init__(self, app:App):
        super().__init__()
        self.app = app
        data_path = self.app.paths.data
        self.bitcoinz_cli_file = os.path.join(data_path, "bitcoinz-cli.exe")
        
    
    async def _run_command(self, command):
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                if stdout:
                    try:
                        data = json.loads(stdout.decode())
                        result = json.dumps(data, indent=4)
                        return result
                    except json.JSONDecodeError:
                        return stdout.decode().strip()
                else:
                    return None
            else:
                error_message = stderr.decode()
                print(f"Command {command} failed with error: {error_message}")
                return None
        except Exception as e:
            print(f"An error occurred while running command {command}: {e}")
            return None
        
    
    async def stopNode(self):
        command = f'{self.bitcoinz_cli_file} stop'
        return await self._run_command(command)       
        
    
    async def getInfo(self):
        command = f'{self.bitcoinz_cli_file} getinfo'
        return await self._run_command(command)
    

    async def getPeerInfo(self):
        command = f'{self.bitcoinz_cli_file} getpeerinfo'
        return await self._run_command(command)
    

    async def getConnectionCount(self):
        command = f'{self.bitcoinz_cli_file} getconnectioncount'
        return await self._run_command(command)
    

    async def getNewAddress(self):
        command = f'{self.bitcoinz_cli_file} getnewaddress'
        return await self._run_command(command)
    

    async def z_getNewAddress(self):
        command = f'{self.bitcoinz_cli_file} z_getnewaddress'
        return await self._run_command(command)
    
                  
    async def z_getTotalBalance(self):
        command = f'{self.bitcoinz_cli_file} z_gettotalbalance'
        return await self._run_command(command)
    
    
    async def z_getBalance(self, address):
        command = f'{self.bitcoinz_cli_file} z_getbalance "{address}"'
        return await self._run_command(command)
    
    async def getAddressBalance(self, address):
        command = f'{self.bitcoinz_cli_file} getaddressbalance "{{\\"addresses\\": [\\"{address}\\"]}}"'
        return await self._run_command(command)
    
    
    async def getBlockchainInfo(self):
        command = f'{self.bitcoinz_cli_file} getblockchaininfo'
        return await self._run_command(command)
    
    
    async def getNetworkSolps(self):
        command = f'{self.bitcoinz_cli_file} getnetworksolps'
        return await self._run_command(command)
    
    
    async def getBestblockhash(self):
        command = f'{self.bitcoinz_cli_file} getbestblockhash'
        return await self._run_command(command)
    
    
    async def getUnconfirmedBalance(self):
        command = f'{self.bitcoinz_cli_file} getunconfirmedbalance'
        return await self._run_command(command)
    
    
    async def getDeprecationInfo(self):
        command = f'{self.bitcoinz_cli_file} getdeprecationinfo'
        return await self._run_command(command)
    
    
    async def getMempoolinfo(self):
        command = f'{self.bitcoinz_cli_file} getmempoolinfo'
        return await self._run_command(command)
    
    
    async def verifyChain(self):
        command = f'{self.bitcoinz_cli_file} verifychain'
        return await self._run_command(command)
    
    
    async def listAddressgroupPings(self):
        command = f'{self.bitcoinz_cli_file} listaddressgroupings'
        return await self._run_command(command)
    

    async def getAddressesByAccount(self):
        command = f'{self.bitcoinz_cli_file} getaddressesbyaccount ""'
        return await self._run_command(command)
    
    
    async def z_listAddresses(self):
        command = f'{self.bitcoinz_cli_file} z_listaddresses'
        return await self._run_command(command)
    
    
    async def validateAddress(self, address):
        command = f'{self.bitcoinz_cli_file} validateaddress {address}'
        return await self._run_command(command)
    
    
    async def z_validateAddress(self, address):
        command = f'{self.bitcoinz_cli_file} z_validateaddress {address}'
        return await self._run_command(command)
    
    
    async def listTransactions(self, count, tx_from):
        command = f'{self.bitcoinz_cli_file} listtransactions "*" {count} {tx_from}'
        return await self._run_command(command)
    
    
    async def getTransaction(self, txid):
        command = f'{self.bitcoinz_cli_file} gettransaction {txid}'
        return await self._run_command(command)
    
    
    async def sendToAddress(self, address, amount, comment):
        if comment:
            command = f'{self.bitcoinz_cli_file} sendtoaddress "{address}" {amount} "{comment}"'
        else:
            command = f'{self.bitcoinz_cli_file} sendtoaddress "{address}" {amount}'
        return await self._run_command(command)
    
    
    async def z_sendMany(self, uaddress, toaddress, amount, comment, txfee):
        if comment:
            hex_comment = binascii.hexlify(comment.encode()).decode()
            command = f'{self.bitcoinz_cli_file} z_sendmany "{uaddress}" "[{{\\"address\\": \\"{toaddress}\\", \\"amount\\": {amount}, \\"memo\\": \\"{hex_comment}\\"}}]" 1 {txfee}'
        else:
            command = f'{self.bitcoinz_cli_file} z_sendmany "{uaddress}" "[{{\\"address\\": \\"{toaddress}\\", \\"amount\\": {amount}}}]" 1 {txfee}'
        
        return await self._run_command(command)

            
    async def z_getOperationStatus(self, operation_ids):
        command = f'{self.bitcoinz_cli_file} z_getoperationstatus "[\\"{operation_ids}\\"]"'
        return await self._run_command(command)
    
    
    async def z_getOperationResult(self, operation_ids):
        command = f'{self.bitcoinz_cli_file} z_getoperationresult "[\\"{operation_ids}\\"]"'
        return await self._run_command(command)
    

    async def getBlock(self, block):
        command = f'{self.bitcoinz_cli_file} getblock "{block}" 2'
        return await self._run_command(command)
    
    
    async def listReceivedByAddress(self):
        command = f'{self.bitcoinz_cli_file} listreceivedbyaddress 0 true'
        return await self._run_command(command)
    
    
    async def getAddressTxids(self, address):
        command = f'{self.bitcoinz_cli_file} getaddresstxids "{{\\"addresses\\": [\\"{address}\\"]}}"'
        return await self._run_command(command)
    
    
    async def getAddressMempool(self, address):
        command = f'{self.bitcoinz_cli_file} getaddressmempool "{{\\"addresses\\": [\\"{address}\\"]}}"'
        return await self._run_command(command)
    
    
    async def getAddressDeltas(self, address):
        command = f'{self.bitcoinz_cli_file} getaddressdeltas "{{\\"addresses\\": [\\"{address}\\"], \\"chainInfo\\": true}}"'
        return await self._run_command(command)
    
    
    async def getTxout(self, txid):
        command = f'{self.bitcoinz_cli_file} gettxout "{txid}" 1'
        return await self._run_command(command)
    
    
    async def getSpentInfo(self, txid):
        command = f'{self.bitcoinz_cli_file} getspentinfo "{{\\"txid\\": \\"{txid}\\", \\"index\\": 4}}"'
        return await self._run_command(command)
    
    
    async def getRawTransaction(self, txid):
        command = f'{self.bitcoinz_cli_file} getrawtransaction "{txid}" 1'
        return await self._run_command(command)
    
    
    async def z_listOperationIds(self):
        command = f'{self.bitcoinz_cli_file} z_listoperationids'
        return await self._run_command(command)
    
    
    async def listUnspent(self, address):
        command = f'{self.bitcoinz_cli_file} listunspent 1 9999999 "[\\"{address}\\"]"'
        return await self._run_command(command)
    
    
    async def z_listUnspent(self, address):
        command = f'{self.bitcoinz_cli_file} z_listunspent 1 9999999 true "[\\"{address}\\"]"'
        return await self._run_command(command)
    

    async def DumpPrivKey(self, address):
        command = f'{self.bitcoinz_cli_file} dumpprivkey "{address}"'
        return await self._run_command(command)
    
    
    async def z_ExportKey(self, address):
        command = f'{self.bitcoinz_cli_file} z_exportkey "{address}"'
        return await self._run_command(command)
    

    async def ImportPrivKey(self, key, rescan):
        if rescan is True:
            command = f'{self.bitcoinz_cli_file} importprivkey "{key}" true'
        else:
            command = f'{self.bitcoinz_cli_file} importprivkey "{key}" false'
        return await self._run_command(command)
    

    async def z_ImportKey(self, key, rescan):
        if rescan is True:
            command = f'{self.bitcoinz_cli_file} z_importkey "{key}" yes'
        else:
            command = f'{self.bitcoinz_cli_file} z_importkey "{key}" no'
        return await self._run_command(command)
    

    async def backupWallet(self, file_name):
        command = f'{self.bitcoinz_cli_file} backupwallet "{file_name}"'
        return await self._run_command(command)
    
    
    async def z_exportWallet(self, file_name):
        command = f'{self.bitcoinz_cli_file} z_exportwallet "{file_name}"'
        return await self._run_command(command)
    

    async def z_importWallet(self, backup_file):
        command = f'{self.bitcoinz_cli_file} z_importwallet "{backup_file}"'
        return await self._run_command(command)
    

    async def z_mergeToaAdress(self, list_addresses, address, tx_fee):
        addresses_json = json.dumps(list_addresses)
        command = f'{self.bitcoinz_cli_file} z_mergetoaddress {addresses_json} {address} {tx_fee}'
        return await self._run_command(command)