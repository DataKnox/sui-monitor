import os
import re
import time
import json
import socket
HOSTNAME = socket.gethostname()
match HOSTNAME:
    case "juicy-sui":
        target_address = "0xcec4dd3fc6f119a10c7524c76fbf06b15d0b527586f9c39d557e7fb4084663ba"
    case "juicy-sui-main":
        target_address = "0xcec4dd3fc6f119a10c7524c76fbf06b15d0b527586f9c39d557e7fb4084663ba"
    case "cypher-testnet":
        active_address = ""
    case "cypher-mainnet":
        active_address = ""
to_file = os.popen(
    '/home/sui/sui/target/debug/sui client objects | grep StakedSui > /home/sui/stake.txt')

time.sleep(5)
with open('/home/sui/stake.txt', 'r') as f:
    second_read = f.readlines()
    for line in second_read:
        stake_obj = line.strip()
        stake_obj_id = stake_obj.split(' ')[0]
        os.popen(
            f'/home/sui/sui/target/debug/sui client call --package 0x3 --module sui_system --function request_withdraw_stake --args 0x5 {stake_obj_id} --gas-budget 20000000')
        time.sleep(5)

to_file = os.popen(
    '/home/sui/sui/target/debug/sui client objects | grep GasCoin > /home/sui/gas.txt')

time.sleep(5)
with open('/home/sui/gas.txt', 'r') as f:
    # Read the file contents and generate a list with each line
    first_line = f.readline()
    match = re.search(r'^\s*([a-zA-Z0-9]+)', first_line)
    if match:
        base_obj = first_line.strip()
        base_obj = base_obj.split(' ')[0]
        print(f"base gas object is {base_obj}")

        second_read = f.readlines()
        for line in second_read:
            if base_obj not in line:
                merging_obj = line.strip()
                merging_obj = merging_obj.split(' ')[0]
                os.popen(
                    f"/home/sui/sui/target/debug/sui client merge-coin --primary-coin {base_obj} --coin-to-merge  {merging_obj} --gas-budget 20000000")
                time.sleep(10)


to_file = os.popen(
    '/home/sui/sui/target/debug/sui client objects | grep GasCoin > /home/sui/gas_new.txt')
time.sleep(5)
with open('/home/sui/gas_new.txt', 'r') as f:
    third_read = f.readlines()
    for line in third_read:
        loop = 1
        obj = line.strip()
        obj_id = obj.split(' ')[0]
        print(line)
        print(obj_id)
        os.popen(
            f'/home/sui/sui/target/debug/sui client object {obj_id} --json > /home/sui/obj.json')
        time.sleep(3)
        g = open('/home/sui/obj.json')
        data = json.load(g)
        balance = round(int(data['content']['fields']['balance']))
        to_send_amt = round(((balance * 0.99)-20000000))
        os.popen(
            f"/home/sui/sui/target/debug/sui client transfer-sui --amount {to_send_amt} --gas-budget 20000000 --sui-coin-object-id {obj_id} --to {active_address} > loop{loop}.txt")
        time.sleep(5)
        loop += 1