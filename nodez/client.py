import os
import requests
import aiohttp
import json
import sqlite3
import binascii

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
    

async def get_btcz_price():
    api_url = "https://api.coinpaprika.com/v1/tickers/btcz-bitcoinz"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    quotes = data.get('quotes', None)
                    btcz_usd = quotes.get('USD', None)
                    price = btcz_usd.get('price', None)
                    return price
                else:
                    print(f"Failed to fetch data. Status code: {response.status}")
    except aiohttp.ClientError as e:
        return None
    except Exception as e:
        return None
    
    
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
            return data
        except Exception as e:
            print(e)
            return None
        
        
    def getInfo(self):
        return self.make_rpc_request(
            "getinfo",
            []
        )
    

    def getConnectionCount(self):
        return self.make_rpc_request(
            "getconnectioncount",
            []
        )
    

    def getNewAddress(self):
        return self.make_rpc_request(
            "getnewaddress",
            []
        )
    

    def z_getNewAddress(self):
        return self.make_rpc_request(
            "z_getnewaddress",
            []
        )
    

    def z_getTotalBalance(self):
        return self.make_rpc_request(
            "z_gettotalbalance",
            []
        )
    

    def getAddressBalance(self, address):
        return self.make_rpc_request(
            "getaddressbalance",
            [{"addresses": [address]}]
        )
    
    def z_getBalance(self, address):
        return self.make_rpc_request(
            "z_getbalance",
            [f"{address}"]
        )
    

    def getBlockchainInfo(self):
        return self.make_rpc_request(
            "getblockchaininfo",
            []
        )
        
    def getNetworkSolps(self):
        return self.make_rpc_request(
            "getnetworksolps",
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
        
    def listAddressgroupPings(self):
        return self.make_rpc_request(
            "listaddressgroupings",
            []
        )
        
    def z_listAddresses(self):
        return self.make_rpc_request(
            "z_listaddresses",
            []
        )
    
    def validateAddress(self, address):
        return self.make_rpc_request(
            "validateaddress",
            [address]
        )
        
    def z_validateAddress(self, address):
        return self.make_rpc_request(
            "z_validateaddress",
            [address]
        )
        
    def listTransactions(self, limit):
        return self.make_rpc_request(
            "listtransactions",
            ["*", limit]
        )
        
    def getTransaction(self, txid):
        return self.make_rpc_request(
            "gettransaction",
            [f"{txid}"]
        )
        
    def sendToAddress(self, address, amount, comment):
        if comment:
            return self.make_rpc_request(
                "sendtoaddress",
                [f"{address}", amount, comment]
            )
        else:
            return self.make_rpc_request(
                "sendtoaddress",
                [f"{address}", amount]
            )
            
        
    def sendMany(self, address, amount, comment):
        if comment:
            return self.make_rpc_request(
                "sendmany",
                ["", {f"\t{address}\t": amount}, 1, comment]
            )
        else:
            return self.make_rpc_request(
                "sendmany",
                ["", {f"\t{address}\t": amount}, 1]
            )
            
        
    def z_sendMany(self, uaddress, toaddress, amount, comment, txfee):
        if comment:
            hex_comment = binascii.hexlify(comment.encode()).decode()
            return self.make_rpc_request(
                "z_sendmany",
                [f"{uaddress}", [{"address": f"{toaddress}", "amount": float(amount), "memo": hex_comment}], 1, float(txfee)]
            )
        else:
            return self.make_rpc_request(
                "z_sendmany",
                [f"{uaddress}", [{"address": f"{toaddress}", "amount": float(amount)}], 1, float(txfee)]
            )
    
    
    def z_getOperationStatus(self, operation):
        return self.make_rpc_request(
            "z_getoperationstatus",
            [[f"{operation}"]]
        )
        
        
    def z_getOperationResult(self, operation):
        return self.make_rpc_request(
            "z_getoperationresult",
            [[f"{operation}"]]
        )
    
    def getBlock(self, block):
        return self.make_rpc_request(
            "getblock",
            [f"{block}", 2]
        )
    

    def getRawTransaction(self, txid):
        return self.make_rpc_request(
            "getrawtransaction",
            [f"{txid}", 1]
        )
    
    
    def getAddressDeltas(self, address):
        return self.make_rpc_request(
            "getaddressdeltas",
            [{"addresses": [address]}]
        )
    
    def listUnspent(self, address):
        return self.make_rpc_request(
            "listunspent",
            [1, 9999999, [address]]
        )
    
    def z_listUnspent(self, address):
        return self.make_rpc_request(
            "z_listunspent",
            [1, 9999999, True, [address]]
        )