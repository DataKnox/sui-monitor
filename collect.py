import time
import boto3
import psutil
import os
import socket
from botocore.config import Config
import requests
import re
DATABASE_NAME = os.environ['DATABASE_NAME']
TABLE_NAME = os.environ['TABLE_NAME']
HOSTNAME = socket.gethostname()

INTERVAL = 5  # Seconds
sui_clock = time.time()


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

        record = prepare_record(current_time)
        record['MeasureValues'].append(prepare_measure('cpu', cpu_utilization))
        record['MeasureValues'].append(
            prepare_measure('memory', memory_utilization))
        record['MeasureValues'].append(
            prepare_measure('swap', swap_utilization))
        record['MeasureValues'].append(
            prepare_measure('disk', disk_utilization))

        records.append(record)

        print("records {} - cpu {} - memory {} - swap {} - disk {}".format(
            len(records), cpu_utilization, memory_utilization,
            swap_utilization, disk_utilization))
        if time.time()-sui_clock > 43200:
            stream = os.popen(
                "/home/sui/sui/target/debug/sui client active-address")
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
                    record.append(prepare_measure('uptime', uptime))
                match = re.search('^highest_synced_checkpoint', line)
                if match:
                    highest_synced_checkpoint = line.strip()
                    record.append(
                        prepare_measure('highest_synced_checkpoint', highest_synced_checkpoint))
                match = re.search('last_synced_checkpoint', line)
                if match:
                    last_synced_checkpoint = line.strip()
                    record.append(
                        prepare_measure('last_synced_checkpoint', last_synced_checkpoint))
            data = requests.post('https://rpc-ws-testnet-w3.suiscan.xyz/',
                                 json={"jsonrpc": "2.0", "id": "1", "method": "sui_getLatestSuiSystemState", "params": []})
            time.sleep(1)
            curr_epoch = data['result']['epoch']
            record.append(prepare_measure('curr_epoch', curr_epoch))
            gas_price = data['result']['gasPrice']
            record.append(prepare_measure('gas_price', gas_price))
            storage_fund = data['result']['storageFund']
            record.append(prepare_measure('storage_fund', storage_fund))
            validator = [v for v in data['result']['validators']
                         if v['suiAddress'] == active_address]
            commission = validator['commissionRate']/100
            record.append(prepare_measure('commission', commission))
            curr_voted_gas = validator['gasPrice']
            record.append(prepare_measure('curr_voted_gas', curr_voted_gas))
            next_epoch_voted_gas = validator['nextEpochGasPrice']
            record.append(
                prepare_measure('next_epoch_voted_gas', next_epoch_voted_gas))
            curr_stake = validator['stakingPoolSuiBalance']/1000000
            record.append(prepare_measure('curr_stake', curr_stake))
            next_epoch_stake = validator['nextEpochStake']/1000000
            record.append(prepare_measure(
                'next_epoch_stake', next_epoch_stake))
            voting_power = validator['votingPower']
            record.append(prepare_measure('voting_power', voting_power))
            rewards_pool = validator['rewardsPool']/1000000
            record.append(prepare_measure('rewards_pool', rewards_pool))
            sui_clock = time.time()
        if len(records) == 10:
            write_records(records, common_attributes)
            records = []

        time.sleep(INTERVAL)