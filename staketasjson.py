import os
import re
import time
import json
import socket
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
HOSTNAME = socket.gethostname()
match HOSTNAME:
    case "juicy-sui":
        target_address = "0xdca53190eeed13263268118ebd1701dc96eba96d3675f3dfb5e7b9b3fae696d5"
    case "juicy-sui-main":
        target_address = "0xdca53190eeed13263268118ebd1701dc96eba96d3675f3dfb5e7b9b3fae696d5"
        rpc_endpoint = "https://rpc-mainnet.suiscan.xyz/"
    case "cypher-testnet":
        target_address = "0xdca53190eeed13263268118ebd1701dc96eba96d3675f3dfb5e7b9b3fae696d5"
        active_address = "0x2081a93bcf642f5964e1f5c4b84e2a22801a62d0137e03d0311ee317163cd27a"
        rpc_endpoint = "https://rpc-testnet.suiscan.xyz/"
    case "cypher-mainnet":
        target_address = "0x5855d61702d7aaf66224a1b70ea6f917445605079bad12a4371e35a575ac0d84"
        rpc_endpoint = "https://rpc-mainnet.suiscan.xyz/"
        active_address = "0xdfc9709adae2917a9be213c8d651b150517fbc8b99106bbd3020e618335ccf18"

def is_first_day_of_month():
    today = datetime.now()
    return today.day == 1

# Example usage
if is_first_day_of_month():
    print("Today is the first day of the month.")
else:
    print("Today is not the first day of the month.")

to_file = os.popen(
    '/home/sui/sui/target/release/sui client objects --json > /home/sui/stake.json')

time.sleep(5)
f = open('/home/sui/stake.json')
data = json.load(f)
for i in data:
    if i["data"]["type"] == '0x3::staking_pool::StakedSui':
        print(i['data']['objectId'])
        os.popen(
            f'/home/sui/sui/target/release/sui client call --package 0x3 --module sui_system --function request_withdraw_stake --args 0x5 {i["data"]["objectId"]} --gas-budget 20000000')
        time.sleep(5)


to_file = os.popen(
    '/home/sui/sui/target/release/sui client gas --json  > /home/sui/gas.json')

time.sleep(5)
fa = open('/home/sui/gas.json')
data = json.load(fa)
print("base coin for merge " + data[0]['gasCoinId'])
os.popen(
    f'/home/sui/sui/target/release/sui client merge-coin --primary-coin {data[0]["gasCoinId"]} --coin-to-merge  {data[1]["gasCoinId"]} --gas-budget 20000000')
time.sleep(5)



to_file = os.popen(
    '/home/sui/sui/target/release/sui client gas --json > /home/sui/gas_new.json')
time.sleep(5)
with open('/home/sui/gas_new.json', 'r') as fs:
    third_read = json.load(fs)
    for line in third_read:
        loop = 0
        os.popen(
            f'/home/sui/sui/target/release/sui client object {line["gasCoinId"]} --json > /home/sui/obj.json')
        time.sleep(3)
        g = open('/home/sui/obj.json')
        data = json.load(g)
        balance = round(int(data['content']['fields']['balance']))
        to_send_amt = round(((balance * 0.99)-20000000))
        if to_send_amt > 0:            
            print(f"to send amount is {str(to_send_amt)} to {target_address} from {line['gasCoinId']}")
            os.popen(
                f'/home/sui/sui/target/release/sui client transfer-sui --amount {to_send_amt} --gas-budget 20000000 --sui-coin-object-id {line["gasCoinId"]} --to {target_address} > loop{loop}.txt')
            time.sleep(5)
        loop += 1

if HOSTNAME in ["cypher-mainnet", "cypher-testnet"]:
    data = requests.post(
        rpc_endpoint,
        json={
            "jsonrpc": "2.0",
            "id": "1",
            "method": "suix_getLatestSuiSystemState",
            "params": [],
        },
    )
    data = data.json()
    validator = [
        v
        for v in data["result"]["activeValidators"]
        if v["suiAddress"] == active_address
         ]
    validator = validator[0]
    curr_stake = validator["stakingPoolSuiBalance"]
    curr_stake = int(curr_stake) / 1000000000
    bitgo_weight = 16460760/curr_stake
    bitgo_share = bitgo_weight*to_send_amt
    payload = {
        "bitgo_share": bitgo_share,
        "total_amount": to_send_amt,
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "isFirst": True if is_first_day_of_month() else False,
    }
    json_payload = json.dumps(payload)
    sent = requests.post(os.getenv("LOGIC"),
                            data=json_payload,headers={'Content-Type': 'application/json'})


