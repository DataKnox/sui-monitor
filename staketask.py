import os
import re
import time
import json
import socket
HOSTNAME = socket.gethostname()
match HOSTNAME:
    case "juicy-sui":
        target_address = "0xdca53190eeed13263268118ebd1701dc96eba96d3675f3dfb5e7b9b3fae696d5"
    case "juicy-sui-main":
        target_address = "0xdca53190eeed13263268118ebd1701dc96eba96d3675f3dfb5e7b9b3fae696d5"
    case "cypher-testnet":
        target_address = ""
    case "cypher-mainnet":
        target_address = "0x5855d61702d7aaf66224a1b70ea6f917445605079bad12a4371e35a575ac0d84"
to_file = os.popen(
    '/home/sui/sui/target/release/sui client objects | grep -B 4 StakedSui > /home/sui/stake.txt')

time.sleep(5)
with open('/home/sui/stake.txt', 'r') as f:
    second_read = f.readlines()
    for line in second_read:
        stake_obj = line.strip()
        stake_obj_eval = stake_obj.split(' ')[3]
        if stake_obj_eval == 'objectId':
            stake_obj_id = stake_obj.split(' ')[5]
            os.popen(
                f'/home/sui/sui/target/release/sui client call --package 0x3 --module sui_system --function request_withdraw_stake --args 0x5 {stake_obj_id} --gas-budget 20000000')
            time.sleep(5)

to_file = os.popen(
    '/home/sui/sui/target/release/sui client sui client gas | grep 0x > /home/sui/gas.txt')

time.sleep(5)
with open('/home/sui/gas.txt', 'r') as f:
    # Read the file contents and generate a list with each line
    first_line = f.readline()
    #match = re.search(r'^\s*([a-zA-Z0-9]+)', first_line)
    # if match:
    base_obj = first_line.strip()
    base_obj = base_obj.split(' ')[1]
    print(f"base gas object is {base_obj}")

    second_read = f.readlines()
    for line in second_read:
        if base_obj not in line:
            merging_obj = line.strip()
            merging_obj = merging_obj.split(' ')[1]
            os.popen(
                f"/home/sui/sui/target/release/sui client merge-coin --primary-coin {base_obj} --coin-to-merge  {merging_obj} --gas-budget 20000000")
            time.sleep(10)


to_file = os.popen(
    '/home/sui/sui/target/release/sui client objects | grep GasCoin > /home/sui/gas_new.txt')
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
            f'/home/sui/sui/target/release/sui client object {obj_id} --json > /home/sui/obj.json')
        time.sleep(3)
        g = open('/home/sui/obj.json')
        data = json.load(g)
        balance = round(int(data['content']['fields']['balance']))
        to_send_amt = round(((balance * 0.99)-20000000))
        os.popen(
            f"/home/sui/sui/target/release/sui client transfer-sui --amount {to_send_amt} --gas-budget 20000000 --sui-coin-object-id {obj_id} --to {target_address} > loop{loop}.txt")
        time.sleep(5)
        loop += 1
