# Import dependencies
import os
import subprocess
import json
from dotenv import load_dotenv
from web3 import Web3

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import BTC, BTCTEST, ETH

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
 
# Create a function called `derive_wallets`
def derive_wallets(# YOUR CODE HERE):
    command = './derive -g --mnemonic="scrub hawk timber mesh cinnamon labor imitate gospel scout tower okay scare" --cols=path,address,privkey,pubkey --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = # YOUR CODE HERE

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(# YOUR CODE HERE):
    # YOUR CODE HERE

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(# YOUR CODE HERE):
    # YOUR CODE HERE

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(# YOUR CODE HERE):
    # YOUR CODE HERE
