import  warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

from datetime import datetime, timezone
from web3 import Web3
import pandas as pd
import json
import time

# contract address and abi details
addressContract = "0x18B2A687610328590Bc8F2e5fEdDe3b582A49cdA"

with open("abi.json", 'r') as abiFile:
    data = abiFile.read()
mainAbiFile = json.loads(data)

print(mainAbiFile)
# provider

rpc_mainnet = "https://data-seed-prebsc-1-s1.binance.org:8545/"

w3 = Web3(Web3.HTTPProvider(rpc_mainnet))
print(w3)