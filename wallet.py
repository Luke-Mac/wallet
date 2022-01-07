# Import dependencies
import os
import subprocess
import json
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("MNEMONIC")


# Import constants.py and necessary functions from bit and web3
from constants import BTC, BTCTEST, ETH

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
 
# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = 'php ./derive -g --mnemonic="{mnemonic}" --coin="{coin}" -- numderive="{numderive}" --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {"eth", "btc-test", "btc"}
numderive = 3

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    if coin == "ETH":
        tx_eth = create_tx(coin, account, recipient, amount)
        signed_tx = account.sign_transaction(tx_eth)
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        #print(result.hex())
        #return result.hex()
    elif coin == "BTCTEST":
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_tx_btctest = account.sign_transaction(tx_btctest)
        return NetworkAPI.broadcast_tx_testnet(signed_tx_btctest)

