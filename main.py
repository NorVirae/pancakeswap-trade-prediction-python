import warnings

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

walletAddress = ""
privateKey = ""
# contract
contract = provider.eth.contract(address=addressContract, abi=mainAbiFile)
# get currentEpoch
current_epoch = contract.functions.currentEpoch().call()
# Take a look back to some 3k epoch
look_back = 3
start_epoch = current_epoch - look_back

rounds_columns = ["epoch", "start_timestamp", "lock_timestamp", "close_timestamp", "lock_price", "close_price",
  "lock_oracle_id", "close_oracle_id", "total_amount", "bull_amount", "bear_amount", "reward_baseCal_amount", "reward_amount",
  "oracle_called", "bull_ratio", "bear_ratio"]

count = 0

excel_frame = pd.DataFrame(columns=rounds_columns)
for e in range(0, look_back):
    time.sleep(1)
    start_epoch += 1
    count += 1
    # fetch round object
    round_list = contract.functions.rounds(start_epoch).call()

    # Name data
    epoch = round_list[0]
    start_timestamp = round_list[1]
    lock_timestamp = round_list[2]
    close_timestamp = round_list[3]
    lock_price = round_list[4]
    close_price = round_list[5]
    lock_oracle_id = round_list[6]
    close_oracle_id = round_list[7]
    total_amount = round_list[8]
    bull_amount = round_list[9]
    bear_amount = round_list[10]
    reward_baseCal_amount = round_list[11]
    reward_amount = round_list[12]
    oracle_called = round_list[13]

    # format data to human readable
    formatted_bull_amount = round(Web3.fromWei(bull_amount, "ether"), 5)
    print(bull_amount, str(formatted_bull_amount) + " BNB")
