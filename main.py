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

# provider

rpc_mainnet = "https://data-seed-prebsc-1-s1.binance.org:8545/"
provider = Web3(Web3.HTTPProvider(rpc_mainnet))

walletAddress = ""
privateKey = ""
# contract
contract = provider.eth.contract(address=addressContract, abi=mainAbiFile)
# get currentEpoch
current_epoch = contract.functions.currentEpoch().call()

# Take a look back to some 3k epoch
lookback = 3
start_epoch = current_epoch - lookback

rounds = ["epoch",
  "start_timestamp",
  "lock_timestam",
  "close_timestamp",
  "lock_price",
  "close_price",
  "lock_oracleId",
  "close_oracleId",
  "total_amount",
  "bull_amount",
  "bear_amount",
  "reward_baseCalAmount",
  "reward_amount",
  "oracle_called",]

count = 1
for e in range(1, lookback):
    time.sleep(1)
    start_epoch += 1
    count += 1
    print(start_epoch, count)