import os
import re
import time
to_file = os.popen(
    '/home/sui/sui/target/debug/sui client objects | grep StakedSui > /home/sui/stake.txt')

time.sleep(5)
with open('/home/sui/stake.txt', 'r') as f:
    second_read = f.readlines()
    for line in second_read:
        print(f"Line: {line}")
        stake_obj = line.strip()
        stake_obj_id = stake_obj.split(' ')[0]
        print("stake obj id:")
        print(stake_obj_id)
        os.popen(
            f'/home/sui/sui/target/debug/sui client call --package 0x3 --module sui_system --function request_withdraw_stake --args 0x5 {stake_obj_id} --gas-budget 20000000')
        time.sleep(5)

to_file = os.popen(
    '/home/sui/sui/target/debug/sui client objects | grep GasCoin > gas.txt')

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
                print(f"Line: {line}")
                merging_obj = line.strip()
                merging_obj = merging_obj.split(' ')[0]
                print("Running:")
                print(
                    f"/home/sui/sui/target/debug/sui client merge-coin --primary-coin {base_obj} --coin-to-merge  {merging_obj} --gas-budget 20000000")
                os.popen(
                    f"/home/sui/sui/target/debug/sui client merge-coin --primary-coin {base_obj} --coin-to-merge  {merging_obj} --gas-budget 20000000")
                time.sleep(10)
