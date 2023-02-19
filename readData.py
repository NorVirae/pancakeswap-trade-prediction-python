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
    print(datetime.fromtimestamp(start_timestamp), "CHECK HERE")
    # format data to human readable
    formatted_bull_amount = round(Web3.fromWei(bull_amount, "ether"), 5)
    formatted_bear_amount = round(Web3.fromWei(bear_amount, "ether"), 5)


    formatted_total_amount = round(Web3.fromWei(total_amount, "ether"), 5)
    formatted_reward_baseCal_amount = round(Web3.fromWei(reward_baseCal_amount, "ether"), 5)
    formatted_reward_amount = round(Web3.fromWei(reward_amount, "ether"), 5)

    # get ratios
    if(bull_amount != 0 and bear_amount != 0):
        bull_ratio = round(formatted_bull_amount / formatted_bear_amount,2 ) + 1
        bear_ratio = round(formatted_bear_amount / formatted_bull_amount, 2) + 1
    else:
        bull_ratio = 0
        bear_ratio = 0

    d_row = {
        "epoch": epoch,
        "start_timestamp": start_timestamp,
        "lock_timestamp": lock_timestamp,
        "close_timestamp": close_timestamp,
        "lock_price": lock_price,
        "close_price": close_price,
        "lock_oracle_id": lock_oracle_id,
        "close_oracle_id": close_oracle_id,
        "total_amount": formatted_total_amount,
        "bull_amount": formatted_bull_amount,
        "bear_amount": formatted_bear_amount,
        "reward_baseCal_amount": formatted_reward_baseCal_amount,
        "reward_amount": formatted_reward_amount,
        "oracle_called": oracle_called,
        "bull_ratio": bull_ratio,
        "bear_ratio":bear_ratio
    }
    try:
        print(d_row)

        excel_frame = excel_frame.append(d_row, ignore_index = True)
        print(excel_frame)
        excel_frame.to_csv("predictions.csv")

    except(e):
        print("Could not append to csv", e)

