

import warnings
from datetime import datetime
from datetime import datetime, timezone
from web3 import Web3
import pandas as pd
import json
import time
warnings.simplefilter(action="ignore", category=FutureWarning)

# contract address and abi details
addressContract = "0x18B2A687610328590Bc8F2e5fEdDe3b582A49cdA"

with open("abi.json", 'r') as abiFile:
    data = abiFile.read()
mainAbiFile = json.loads(data)

# provider

rpc_mainnet = "https://bsc-dataseed.binance.org/"
provider = Web3(Web3.HTTPProvider(rpc_mainnet))

walletAddress = "0xBC5B9D64284fA4B723d085Acbe543C01721E75B4"
privateKey = ""
# contract
contract = provider.eth.contract(address=addressContract, abi=mainAbiFile)
# get currentEpoch
current_epoch = contract.functions.currentEpoch().call()
# Take a look back to some 3k epoch
look_back = 100
start_epoch = current_epoch - look_back

rounds_columns = ["epoch", "start_timestamp", "lock_timestamp", "close_timestamp", "lock_price", "close_price",
  "lock_oracle_id", "close_oracle_id", "total_amount", "bull_amount", "bear_amount", "reward_baseCal_amount", "reward_amount",
  "oracle_called", "bull_ratio", "bear_ratio"]

count = 0

excel_frame = pd.DataFrame(columns=rounds_columns)
