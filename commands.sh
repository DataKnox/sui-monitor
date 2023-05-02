# get sui validator states
curl --location --request POST 'https://rpc-mainnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getLatestSuiSystemState",
  "params": [ "0x5"]
}'

# jq 
curl -X POST -H "Content-Type: application/json" --data '{ "jsonrpc":"2.0", "method":"suix_getLatestSuiSystemState","id":1, "params": [ "0x5"]}' https://sui-rpc-mainnet.testnet-pride.com:443 | jq '[.result.activeValidators[] | select( .name=="Juicy Stake" or .name=="Cypher Capital") | {name,nextEpochStake,votingPower,nextEpochCommissionRate,nextEpochGasPrice}]'

# basic metrics
curl -s localhost:9184/metrics | grep -e ^current_round -e ^uptime -e ^highest_synced_checkpoint -e ^last_executed_checkpoint 

# get self stake MAINNET 
curl --location --request POST 'https://rpc-mainnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getStakes",
  "params": [ "Your address here"]
}'


# TESTNET
curl --location --request POST 'https://rpc-testnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getStakes",
  "params": [ "0x407f2bd2d36f40e57e4b725e7b80d4afc588fd2deb746ad62ccc6ed086798e48"]
}'

# get all coins 
curl --location --request POST 'https://rpc-testnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getAllCoins",
  "params": [ "0x407f2bd2d36f40e57e4b725e7b80d4afc588fd2deb746ad62ccc6ed086798e48"]
}'

# get all balances 
curl --location --request POST 'https://rpc-testnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getAllBalances",
  "params": [ "0x407f2bd2d36f40e57e4b725e7b80d4afc588fd2deb746ad62ccc6ed086798e48"]
}'
# merge stake?
sui client call --package 0x3 --module staking_pool --function join_staked_sui --args 0x63952d1ac7f1ce2d864f51315d0bf1317ec8851f5389a54961b3ecf2b732e540 0x665b699c1aefff1244a07133d00f72ed6994cdc74982b2bac6ee84bd7cc622a1 --gas-budget 20000000

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
sui client merge-coin --primary-coin 0x00b20cf8d489c2c1237cddb47b039b28e7b855aec78529763e71285e406f8978 --coin-to-merge  0x116edf3ea308e245c29b1b6724e0fba8b17781d3488c375876025481802d3247 --gas-budget 20000000 --gas 0x38c9ce9fb4a1a934d3a0935299f3fa0fd88656b4a15d9170e116793e5af62f71
sui client merge-coin --primary-coin 0xf3b9...3a3bc --coin-to-merge  0xe6e...0ae --gas-budget 20000000 --gas 0x1830...148

# withdraw stake
sui client call --package 0x3 --module sui_system --function request_withdraw_stake --args 0x5 0xde589384b3d7e0b2ee40be9806173f5e3f4bbde57fdea80785740d752f5498f1 --gas-budget 20000000

# transfer
sui client transfer-sui --amount 100000000 --gas-budget 20000000 --sui-coin-object-id 0x972ef681d82928f433514163505f924f45689c0fd016b1029c4e46dd4302f182 --to 0xdca53190eeed13263268118ebd1701dc96eba96d3675f3dfb5e7b9b3fae696d5

# set gas price
sui validator update-gas-price 901

#tally 
sui client call --package 0x3 --module sui_system --function report_validator --args 0x5 Cap_Id Validator_Address_toReport --gas-budget 20000000 --gas 0x059c1c08e9d7065d7f4be078d3e54e5755a842273317b2ccc27b1f3e821b06d5
sui client call --package 0x3 --module sui_system --function report_validator --args 0x5 0xbe8439523a061fededfabb9925c527ea4110ccd44fad120e16e968a60b6dd9a3 0x6d6e9f9d3d81562a0f9b767594286c69c21fea741b1c2303c5b7696d6c63618a --gas-budget 20000000 --gas 0x059c1c08e9d7065d7f4be078d3e54e5755a842273317b2ccc27b1f3e821b06d5