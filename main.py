

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
currentEpoch = contract.functions.currentEpoch().call()
# send transaction
def sendTx(tradeSide):
    chainId = 56
    gas = 300000
    gas_price = Web3.toWei('5.5', "gwei")
    readHumanAmount = '0.01'
    amount = Web3.toWei(readHumanAmount, "ether")
    nonce = provider.eth.getTransactionCount(walletAddress)

    #build transaction
    if tradeSide == 'bull':
        to_be_sent = contract.functions.betBear(currentEpoch).buildTransaction({
            'chainId':chainId,
            'value': amount,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce
        })

    if tradeSide == 'bear':
        to_be_sent = contract.functions.betBull(currentEpoch).buildTransaction({
            'chainId':chainId,
            'value': amount,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce
        })

    # sign the transaction

    signed_tx = provider.eth.account.signTransaction(to_be_sent, private_key=privateKey)

    #send transaction
    sent_tx = provider.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(sent_tx)

def look_to_trade():
    get_round_data = contract.functions.rounds(currentEpoch).call()
    bull_amount = get_round_data[9]
    bear_amount = get_round_data[10]
    total_amount = get_round_data[8]
    lock_timestamp = get_round_data[2]
    dt = datetime.now().timestamp()
    time_remaining = lock_timestamp - dt


    #get ratios
    if(bull_amount>0 and bear_amount > 0):
        bull_ratio = bull_amount/bear_amount
        bear_ratio = bear_amount/bull_amount
    else:
        bull_ratio = 0
        bear_ratio = 0

    if time_remaining < 10:
        if bull_ratio > bear_ratio:
            sendTx("bull")
        else:
            sendTx("bear")
#
def claim_winnings(epoch):
    chainId = 56
    gas = 300000
    gas_price = Web3.toWei('5.5', "gwei")
    nonce = provider.eth.getTransactionCount(walletAddress)

    # build transaction
    to_be_sent = contract.functions.claim(epoch).buildTransaction({
        'chainId': chainId,
        'gas': gas,
        'gasPrice': gas_price,
        'nonce': nonce
    })
look_to_trade()