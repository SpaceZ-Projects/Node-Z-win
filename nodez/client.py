import os
import asyncio
import urllib.request
import json
import sqlite3
import binascii
import http.client
import base64

from toga import App

    
def rpc_test(rpcuser, rpcpassword, rpchost, rpcport):
    try:
        conn = http.client.HTTPConnection(rpchost, rpcport)
        payload = {
            "jsonrpc": "1.0",
            "id": "curltest",
            "method": "getinfo",
            "params": [],
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Basic " + base64.b64encode(f"{rpcuser}:{rpcpassword}".encode()).decode(),
        }
        conn.request("POST", "/", json.dumps(payload), headers)
        response = conn.getresponse()
        
        if response.status == 200:
            return True
        else:
            return False
    
    except http.client.HTTPException as e:
        print(f"HTTPException: {e}")
        return False
    
    except ConnectionRefusedError:
        print(f"Connection refused to {rpchost}:{rpcport}. Is the RPC server running?")
        return False
    
    except Exception as e:
        print(f"Exception: {e}")
        return False
    
    finally:
        if conn:
            conn.close()


async def get_btcz_price():
    api_url = "https://api.coinpaprika.com/v1/tickers/btcz-bitcoinz"
    try:
        response = await fetch_url(api_url)
        if response:
            data = json.loads(response)
            quotes = data.get('quotes', None)
            btcz_usd = quotes.get('USD', None)
            price = btcz_usd.get('price', None)
            return price
        else:
            print("Failed to fetch data.")
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    

async def fetch_url(url):
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, urllib.request.urlopen, url)
    response = await future
    return response.read()
    
    
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
        payload = {
            "jsonrpc": "1.0",
            "id": "curltest",
            "method": method,
            "params": params,
        }
        payload_json = json.dumps(payload)

        conn = http.client.HTTPConnection(rpchost, rpcport)
        try:
            credentials = f"{rpcuser}:{rpcpassword}"
            encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            auth_header = f"Basic {encoded_credentials}"

            conn.request("POST", "/", payload_json, {
                "Content-type": "text/plain",
                "Authorization": auth_header,
            })
            response = conn.getresponse()
            data = json.loads(response.read().decode())
            if "result" in data:
                return data["result"]
            else:
                print("RPC request failed:", data.get("error"))
                return None

        except http.client.HTTPException as e:
            print(f"HTTPException: {e}")
            return False
        
        except ConnectionRefusedError:
            print(f"Connection refused to {rpchost}:{rpcport}. Is the RPC server running?")
            return False
        
        except Exception as e:
            print(f"Exception: {e}")
            return False
        
        finally:
            if conn:
                conn.close()
        
        
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
    
    def getAddressesByAccount(self):
        return self.make_rpc_request(
            "getaddressesbyaccount",
            [""]
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
        
    def listTransactions(self, count, tx_from):
        return self.make_rpc_request(
            "listtransactions",
            ["*", count, tx_from]
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
    
    def DumpPrivKey(self, address):
        return self.make_rpc_request(
            "dumpprivkey",
            [f"{address}"]
        )

    def z_ExportKey(self, address):
        return self.make_rpc_request(
            "z_exportkey",
            [f"{address}"]
        )
    
    def ImportPrivKey(self, key, rescan):
        if rescan is True:
            return self.make_rpc_request(
                "importprivkey",
                [f"{key}", True]
            )
        else:
            return self.make_rpc_request(
                "importprivkey",
                [f"{key}", False]
            )
        
    def z_ImportKey(self, key, rescan):
        if rescan is True:
            return self.make_rpc_request(
                "z_importkey",
                [f"{key}", "yes"]
            )
        else:
            return self.make_rpc_request(
                "z_importkey",
                [f"{key}", "no"]
            )
        
    
    def z_exportWallet(self, file_name):
        return self.make_rpc_request(
            "z_exportwallet",
            [f"{file_name}"]
        )
    

    def z_importWallet(self, backup_file):
        return self.make_rpc_request(
            "z_importwallet",
            [f"{backup_file}"]
        )
    

    def z_mergeToaAdress(self, list_addresses, address, tx_fee, limit):
        addresses_json = json.dumps(list_addresses)
        return self.make_rpc_request(
            "z_mergetoaddress",
            [addresses_json, address, tx_fee, limit]
        )