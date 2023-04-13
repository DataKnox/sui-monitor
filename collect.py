import time
import boto3
import psutil
import os
import socket
from botocore.config import Config
import requests
import re
# DATABASE_NAME = os.environ['DATABASE_NAME']
# TABLE_NAME = os.environ['TABLE_NAME']
HOSTNAME = socket.gethostname()
TABLE_NAME = "suimon"
DATABASE_NAME = "testDB"
INTERVAL = 5  # Seconds
sui_clock = time.time()
first_run = True


def prepare_common_attributes():
    common_attributes = {
        'Dimensions': [
            {'Name': 'hostname', 'Value': HOSTNAME}
        ],
        'MeasureName': 'utilization',
        'MeasureValueType': 'MULTI'
    }
    return common_attributes


def prepare_record(current_time):
    record = {
        'Time': str(current_time),
        'MeasureValues': []
    }
    return record


def prepare_measure(measure_name, measure_value):
    measure = {
        'Name': measure_name,
        'Value': str(measure_value),
        'Type': 'DOUBLE'
    }
    return measure


def write_records(records, common_attributes):
    try:
        result = write_client.write_records(DatabaseName=DATABASE_NAME,
                                            TableName=TABLE_NAME,
                                            CommonAttributes=common_attributes,
                                            Records=records)
        status = result['ResponseMetadata']['HTTPStatusCode']
        print("Processed %d records. WriteRecords HTTPStatusCode: %s" %
              (len(records), status))
    except Exception as err:
        print("Error:", err)


if __name__ == '__main__':

    print("writing data to database {} table {}".format(
        DATABASE_NAME, TABLE_NAME))

    session = boto3.Session()
    write_client = session.client('timestream-write', config=Config(
        read_timeout=20, max_pool_connections=5000, retries={'max_attempts': 10}))
    query_client = session.client('timestream-query')  # Not used

    common_attributes = prepare_common_attributes()

    records = []

    while True:

        current_time = int(time.time() * 1000)
        cpu_utilization = psutil.cpu_percent()
        memory_utilization = psutil.virtual_memory().percent
        swap_utilization = psutil.swap_memory().percent
        disk_utilization = psutil.disk_usage('/').percent
        db_utilization = psutil.disk_usage('/opt/sui/db').percent
        record = prepare_record(current_time)
        record['MeasureValues'].append(prepare_measure('cpu', cpu_utilization))
        record['MeasureValues'].append(
            prepare_measure('memory', memory_utilization))
        record['MeasureValues'].append(
            prepare_measure('swap', swap_utilization))
        record['MeasureValues'].append(
            prepare_measure('disk', disk_utilization))
        record['MeasureValues'].append(
            prepare_measure('db_disk', db_utilization))
        records.append(record)

        print("records {} - cpu {} - memory {} - swap {} - disk {}".format(
            len(records), cpu_utilization, memory_utilization,
            swap_utilization, disk_utilization))
        stream = os.popen(
            'curl -s localhost:9184/metrics -o /home/sui/sui-monitor/output.txt')
        time.sleep(1)
        with open('/home/sui/sui-monitor/output.txt', 'r') as f:
            # Read the file contents and generate a list with each line
            lines = f.readlines()

            for line in lines:
                match = re.search('^uptime', line)
                if match:
                    uptime = line.strip()
                    uptime = uptime.rsplit(' ', 1)[-1]
                    record['MeasureValues'].append(
                        prepare_measure('uptime', uptime))
                match = re.search('^highest_synced_checkpoint', line)
                if match:
                    highest_synced_checkpoint = line.strip()
                    highest_synced_checkpoint = highest_synced_checkpoint.rsplit(
                        ' ', 1)[-1]
                    record['MeasureValues'].append(
                        prepare_measure('highest_synced_checkpoint', highest_synced_checkpoint))
                match = re.search('^certificates_created', line)
                if match:
                    certificates_created = line.strip()
                    certificates_created = certificates_created.rsplit(
                        ' ', 1)[-1]
                    record['MeasureValues'].append(
                        prepare_measure('certificates_created', certificates_created))
                match = re.search('^last_executed_checkpoint', line)
                if match:
                    last_executed_checkpoint = line.strip()
                    last_executed_checkpoint = last_executed_checkpoint.rsplit(
                        ' ', 1)[-1]
                    record['MeasureValues'].append(
                        prepare_measure('last_executed_checkpoint', last_executed_checkpoint))
                match = re.search('^current_round', line)
                if match:
                    current_round = line.strip()
                    current_round = current_round.rsplit(
                        ' ', 1)[-1]
                    record['MeasureValues'].append(
                        prepare_measure('current_round', current_round))
        # os.remove('output.txt')
        if (time.time()-sui_clock > 43200) or first_run:
            first_run = False
            print("sui time elapsed")
            # stream = os.popen(
            #     "/home/sui/sui/target/debug/sui client active-address")
            # active_address = stream.read()
            # active_address = active_address.strip()
            # print(active_address.strip())
            active_address = '0xb7847468db546ba85acb9dcdc0c5190b3ca6427d713ff52a4f8183c81f8a39e1'

            data = requests.post('https://rpc-mainnet.suiscan.xyz/',
                                 json={"jsonrpc": "2.0", "id": "1", "method": "suix_getLatestSuiSystemState", "params": []})
            time.sleep(1)
            data = data.json()
            # pool_token_balance = data['result']['poolTokenBalance']
            # record['MeasureValues'].append(
            #     prepare_measure('pool_token_balance', pool_token_balance))
            curr_epoch = data['result']['epoch']
            record['MeasureValues'].append(
                prepare_measure('curr_epoch', curr_epoch))
            gas_price = data['result']['referenceGasPrice']
            record['MeasureValues'].append(
                prepare_measure('gas_price', gas_price))
            # storage_fund = data['result']['storageFund']
            # record['MeasureValues'].append(
            #     prepare_measure('storage_fund', storage_fund))
            validator = [v for v in data['result']['activeValidators']
                         if v['suiAddress'] == active_address]
            validator = validator[0]
            commission = validator['commissionRate']
            commission = int(commission)/100
            record['MeasureValues'].append(
                prepare_measure('commission', commission))
            curr_voted_gas = validator['gasPrice']
            record['MeasureValues'].append(
                prepare_measure('curr_voted_gas', curr_voted_gas))
            next_epoch_voted_gas = validator['nextEpochGasPrice']
            record['MeasureValues'].append(
                prepare_measure('next_epoch_voted_gas', next_epoch_voted_gas))
            curr_stake = validator['stakingPoolSuiBalance']
            curr_stake = int(curr_stake)/1000000000
            record['MeasureValues'].append(
                prepare_measure('curr_stake', curr_stake))
            next_epoch_stake = validator['nextEpochStake']
            next_epoch_stake = int(next_epoch_stake)/1000000000
            record['MeasureValues'].append(prepare_measure(
                'next_epoch_stake', next_epoch_stake))
            voting_power = validator['votingPower']
            record['MeasureValues'].append(
                prepare_measure('voting_power', voting_power))
            rewards_pool = validator['rewardsPool']
            rewards_pool = int(rewards_pool)/1000000000
            record['MeasureValues'].append(
                prepare_measure('rewards_pool', rewards_pool))
            data = requests.post('https://rpc-mainnet.suiscan.xyz/',
                                 json={
                                     "jsonrpc": "2.0",
                                     "id": 1,
                                     "method": "suix_getStakes",
                                     "params": [active_address]
                                 })
            time.sleep(1)
            data = data.json()['result'][0]['stakes']
            stake_total = 0
            if data:
                for s in data:
                    stake_total += s['principal']
                record['MeasureValues'].append(
                    prepare_measure('stake_total', stake_total/1000000000))
            sui_clock = time.time()
            print(record)
        else:
            print("not time yet")
            record['MeasureValues'].append(
                prepare_measure('rewards_pool', rewards_pool))
            record['MeasureValues'].append(
                prepare_measure('voting_power', voting_power))
            record['MeasureValues'].append(prepare_measure(
                'next_epoch_stake', next_epoch_stake))
            record['MeasureValues'].append(
                prepare_measure('curr_stake', curr_stake))
            record['MeasureValues'].append(
                prepare_measure('next_epoch_voted_gas', next_epoch_voted_gas))
            record['MeasureValues'].append(
                prepare_measure('curr_voted_gas', curr_voted_gas))
            record['MeasureValues'].append(
                prepare_measure('commission', commission))
            # record['MeasureValues'].append(
            #     prepare_measure('storage_fund', storage_fund))
            record['MeasureValues'].append(
                prepare_measure('gas_price', gas_price))
            record['MeasureValues'].append(
                prepare_measure('curr_epoch', curr_epoch))
            # record['MeasureValues'].append(
            #     prepare_measure('pool_token_balance', pool_token_balance))
            record['MeasureValues'].append(
                prepare_measure('stake_total', stake_total/1000000))
            # record['MeasureValues'].append(
            #     prepare_measure('last_synced_checkpoint', last_synced_checkpoint))
        if len(records) == 10:
            write_records(records, common_attributes)
            records = []

        time.sleep(INTERVAL)
