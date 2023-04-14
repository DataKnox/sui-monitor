# get sui validator states
curl --location --request POST 'https://rpc-mainnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getLatestSuiSystemState",
  "params": [ "0x5"]
}'

# basic metrics
curl -s localhost:9184/metrics | grep -e ^current_round -e ^uptime -e ^highest_synced_checkpoint -e ^last_executed_checkpoint 

# get self stake
curl --location --request POST 'https://rpc-mainnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getStakes",
  "params": [ "0xb7847468db546ba85acb9dcdc0c5190b3ca6427d713ff52a4f8183c81f8a39e1"]
}'

# self stake
sui client call --package 0x3 --module sui_system --function request_add_stake --args 0x5 0x23209625ec80d9adc296edfee386511a0fc7b370b9b8b944df29e976583d5320 0xbb5f4cee78b552ae10f6f7891ec168dfbef870fad139b815ce3b6fba17823ab5 --gas 0x1830f5cef753277180773be0f29e60a0605b3cc4b87f7f1e4829d355eba24148 --gas-budget 20000000
# set commission rate
sui client call --package 0x3 --module sui_system --function request_set_commission_rate --args 0x5 900 --gas-budget 20000000
# unstake
sui client call --package 0x3 --module sui_system --function request_withdraw_stake --args 0x5 0x204bb801744a27fc60f3b94b98ca5d842c908e7446d7891498b5cd96853aeb90 --gas 0x38c9ce9fb4a1a934d3a0935299f3fa0fd88656b4a15d9170e116793e5af62f71 --gas-budget 20000000

# get gas objects
sui client gas
# merge coins
sui client merge-coin --primary-coin <target> coin-to-merge <source> --gas-budget 20_000_000 --gas <gas object paying for gas>
sui client merge-coin --primary-coin 0x7983914e8020aea14d4f615c8405752d0d3900575806fec877f0f2a10525074a --coin-to-merge  0xeb5c74c0fb1a40feea0ddc5ec1a5bc19eb8c13c06ccac3baf59ed33656aa8310 --gas-budget 20000000 --gas 0x38c9ce9fb4a1a934d3a0935299f3fa0fd88656b4a15d9170e116793e5af62f71
sui client merge-coin --primary-coin 0xf3b9...3a3bc --coin-to-merge  0xe6e...0ae --gas-budget 20000000 --gas 0x1830...148


# set gas price
sui validator update-gas-price 901