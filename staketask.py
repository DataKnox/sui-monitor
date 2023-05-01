import os
import re
import time
to_file = os.popen(
    '/home/sui/sui/target/debug/sui client objects | grep StakedSui > /home/sui/stake.txt')

time.sleep(5)
with open('/home/sui/gas.txt', 'r') as f:
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
