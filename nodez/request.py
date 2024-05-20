import os
import requests
import json
import sqlite3

from toga import App

    
def rpc_test(rpcuser, rpcpassword, rpchost, rpcport):
    try:
        url = f"http://{rpchost}:{rpcport}"
        headers = {"content-type": "text/plain"}
        payload = {
            "jsonrpc": "1.0",
            "id": "curltest",
            "method": "getinfo",
            "params": [],
        }
        response = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            auth=(rpcuser, rpcpassword),
        )
        if response.status_code == 200:
            return True
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
        return False
    
    
class RPCRequest():
    def __init__(self, app:App):
        super().__init__()
        self.app = app
        
    def rpc_config(self):
        config_path = self.app.paths.config
        if not os.path.exists(config_path):
            return None
        config_file = os.path.join(config_path, 'config.db')
        if not os.path.exists(config_file):
            return None
        conn = sqlite3.connect(config_file)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT rpcuser, rpcpassword, rpchost, rpcport FROM config"
        )
        result = cursor.fetchone()
        conn.close()
        rpcuser, rpcpassword, rpchost, rpcport = result
        return rpcuser, rpcpassword, rpchost, rpcport
    
    def make_rpc_request(self, method, params):
        rpcuser, rpcpassword, rpchost, rpcport = self.rpc_config()
        url = f"http://{rpchost}:{rpcport}"
        headers = {"content-type": "text/plain"}
        payload = {
            "jsonrpc": "1.0",
            "id": "curltest",
            "method": method,
            "params": params,
        }
        try:
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
                auth=(rpcuser, rpcpassword),
            )
            response.raise_for_status()
            data = response.json()["result"]
            print(data)
            return data
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            return None
        
    def getInfo(self):
        return self.make_rpc_request(
            "getinfo",
            []
        )
    def Z_getTotalBalance(self):
        return self.make_rpc_request(
            "z_gettotalbalance",
            []
        )
    def Z_getBalance(self, address):
        return self.make_rpc_request(
            "z_getbalance",
            [f"{address}"]
        )
    def getBlockchainInfo(self):
        return self.make_rpc_request(
            "getblockchaininfo",
            []
        )
        
    def getBestblockhash(self):
        return self.make_rpc_request(
            "getbestblockhash",
            []
        )
        
    def getUnconfirmedBalance(self):
        return self.make_rpc_request(
            "getunconfirmedbalance",
            []
        )
        
    def getDeprecationInfo(self):
        return self.make_rpc_request(
            "getdeprecationinfo",
            []
        )
        
    def getMempoolinfo(self):
        return self.make_rpc_request(
            "getmempoolinfo",
            []
        )
        
    def verifyChain(self):
        return self.make_rpc_request(
            "verifychain",
            []
        )
    
    def validateAddress(self, address):
        return self.make_rpc_request(
            "validateaddress",
            [address]
        )
        
    def Z_validateAddress(self, address):
        return self.make_rpc_request(
            "z_validateaddress",
            [address]
        )
        
    def listTransactions(self):
        return self.make_rpc_request(
            "listtransactions",
            ["*", 10]
        )
        
    def getTransaction(self, txid):
        return self.make_rpc_request(
            "gettransaction",
            [f"{txid}"]
        )