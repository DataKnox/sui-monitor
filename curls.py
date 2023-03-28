import os
import re
import time
import requests
stream = os.popen("/home/sui/sui/target/debug/sui client active-address")
active_address = stream.read()
# print(active_address.strip())
active_address = '0x8925c11a13cf4b30a64a30ee9f3ca401e58b541b34517d99122e779aa81e3bc9'
stream = os.popen('curl -s localhost:9184/metrics -o output.txt')
time.sleep(1)
with open('output.txt', 'r') as f:
    # Read the file contents and generate a list with each line
    lines = f.readlines()


for line in lines:
    match = re.search('^uptime', line)
    if match:
        uptime = line.strip()
    match = re.search('^highest_synced_checkpoint', line)
    if match:
        highest_synced_checkpoint = line.strip()
    match = re.search('^last_synced_checkpoint', line)
    if match:
        last_synced_checkpoint = line.strip()

# print(f"and uptime {uptime} for {active_address}")

data = requests.post('https://rpc-ws-testnet-w3.suiscan.xyz/',
                     json={"jsonrpc": "2.0", "id": "1", "method": "sui_getLatestSuiSystemState", "params": []})
time.sleep(1)
curr_epoch = data['result']['epoch']
gas_price = data['result']['gasPrice']
storage_fund = data['result']['storageFund']
validator = [v for v in data['result']['validators']
             if v['suiAddress'] == active_address]
commission = str(validator['commissionRate']/100)+'%'
curr_voted_gas = validator['gasPrice']
next_epoch_voted_gas = validator['nextEpochGasPrice']
curr_stake = validator['stakingPoolSuiBalance']/1000000
next_epoch_stake = validator['nextEpochStake']/1000000
voting_power = validator['votingPower']
rewards_pool = validator['rewardsPool']/1000000
