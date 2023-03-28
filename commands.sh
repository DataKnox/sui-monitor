# get sui validator states
curl --location --request POST 'https://rpc-testnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getLatestSuiSystemState",
  "params": [ "0x5"]
}'

# basic metrics
curl -s localhost:9184/metrics | grep -e ^current_round -e ^uptime -e ^highest_synced_checkpoint -e ^last_executed_checkpoint

# get self stake
curl --location --request POST 'https://rpc-testnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sui_getStakes",
  "params": [ "0xbb5f4cee78b552ae10f6f7891ec168dfbef870fad139b815ce3b6fba17823ab5"]
}'

# self stake
sui client call --package 0x2 --module sui_system --function request_add_stake --args 0x5 0x23209625ec80d9adc296edfee386511a0fc7b370b9b8b944df29e976583d5320 0xbb5f4cee78b552ae10f6f7891ec168dfbef870fad139b815ce3b6fba17823ab5 --gas 0x1830f5cef753277180773be0f29e60a0605b3cc4b87f7f1e4829d355eba24148 --gas-budget 20000000
# set commission rate
sui client call --package 0x2 --module sui_system --function request_set_commission_rate --args 0x5 1500 --gas-budget 20000000

# get gas objects
sui client gas
# merge coins
sui client merge-coin --primary-coin <target> coin-to-merge <source> --gas-budget 20_000_000 --gas <gas object paying for gas>
sui client merge-coin --primary-coin 0x437dd78a8970cec303a329f1ae1876b03b494a90f0a6474c7c052ae923eafc9d --coin-to-merge  0xbcca11f06f07d6cca8927d111de2820dcb73ab943b91795c0753f0d521266ca7 --gas-budget 20000000 --gas 0x1830f5cef753277180773be0f29e60a0605b3cc4b87f7f1e4829d355eba24148
sui client merge-coin --primary-coin 0xf3b9...3a3bc --coin-to-merge  0xe6e...0ae --gas-budget 20000000 --gas 0x1830...148


# set gas price
sui client call --package 0x2 --module sui_system --function request_set_gas_price --args 0x5 0xcffcbbf637ac80bfab74fa43b2538ce97109959d49b738929bf9a087b262ca12 900 --gas-budget 20000000 --gas 0x1830f5cef753277180773be0f29e60a0605b3cc4b87f7f1e4829d355eba24148