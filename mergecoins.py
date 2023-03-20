import json
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()
env = os.getenv("ENV")
merge_command = """/home/sui/sui/target/release/sui client merge-coin --primary-coin $1 --coin-to-merge $2 --gas-budget 1990000000 --gas $3"""


def gas_out():
    with open("gas.json", "w") as f:
        subprocess.call(["/home/sui/sui/target/release/sui",
                        "client", "gas", "--json"], stdout=f)
    gas_objs = list(reversed(json.loads(open("gas.json").read())))
    return gas_objs


if env == "test":
    gas_objs = list(reversed(json.loads(open("gas.json").read())))
else:
    gas_objs = gas_out()
# stake_command = """/home/sui/sui/target/release/sui client call --package 0x2 --module sui_system --function request_add_stake --args 0x5 \"$1\" --gas $2 --gas-budget 15000"""
while len(gas_objs) > 1:
    id1 = gas_objs[0]["id"]["id"]
    id2 = gas_objs[1]["id"]["id"]
    formed_merge_command = merge_command.replace(
        "$1", id1).replace("$2", id2).replace("$3", id1)
    print(formed_merge_command.split(" "))
    subprocess.call(formed_merge_command.split(" "))
    gas_objs = gas_out()
