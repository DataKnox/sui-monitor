import os
import re
import time
to_file = os.popen(
    '/home/sui/sui/target/debug/sui client objects | grep StakedSui > stake.txt')

time.sleep(5)
with open('/home/sui/gas.txt', 'r') as f:
    second_read = f.readlines()
    for line in second_read:
        print(f"Line: {line}")
        merging_obj = line.strip()
        merging_obj = merging_obj.split(' ')[0]
        print("merging:\n")
        print(merging_obj)
