# get sui validator states
curl --location --request POST 'https://rpc-mainnet.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getLatestSuiSystemState",
  "params": [ "0x5"]
}'

# jq 
curl -X POST -H "Content-Type: application/json" --data '{ "jsonrpc":"2.0", "method":"suix_getLatestSuiSystemState","id":1, "params": [ "0x5"]}' https://sui-rpc-mainnet.testnet-pride.com:443 | jq '[.result.activeValidators[] | select( .name=="Juicy Stake" or .name=="Cypher Capital") | {name,nextEpochStake,votingPower,nextEpochCommissionRate,nextEpochGasPrice, suiAddress}]'

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
sui client call --package 0x3 --module sui_system --function request_set_commission_rate --args 0x5 800 --gas-budget 20000000
# unstake
sui client call --package 0x3 --module sui_system --function request_withdraw_stake --args 0x5 0x204bb801744a27fc60f3b94b98ca5d842c908e7446d7891498b5cd96853aeb90 --gas 0x38c9ce9fb4a1a934d3a0935299f3fa0fd88656b4a15d9170e116793e5af62f71 --gas-budget 20000000

# get gas objects
sui client gas
# merge coins
sui client merge-coin --primary-coin <target> coin-to-merge <source> --gas-budget 20_000_000 --gas <gas object paying for gas>
sui client merge-coin --primary-coin 0x0da6bfe2a22c4607772eb3eda85fe17d69b2a4a1a20e6e1c1906277bc51b3992 --coin-to-merge  0x22a008cdfe3772e8697e57528329650c7bb66a85bf69995afdd132c3a32d1268 --gas-budget 15000000 --gas 0x0da6bfe2a22c4607772eb3eda85fe17d69b2a4a1a20e6e1c1906277bc51b3992
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

# tally juicy 
curl -X POST -H "Content-Type: application/json" --data '{ "jsonrpc":"2.0", "method":"suix_getLatestSuiSystemState","id":1, "params": [ "0x5"]}' https://sui-rpc-mainnet.testnet-pride.com:443 | jq '[.result.activeValidators[] | select( .name=="Kiln" or .name=="BlockEden.xyz") | {name,nextEpochStake,votingPower,nextEpochCommissionRate,nextEpochGasPrice, suiAddress}]'

sui client call --package 0x3 --module sui_system --function report_validator --args 0x5 0x415224057e86d9430e5cb91b98c6c9c10b8595be25b7f755b82d19e6674ec12f 0x3b5664bb0f8bb4a8be77f108180a9603e154711ab866de83c8344ae1f3ed4695 --gas-budget 20000000 --gas 0x06ddb5d91937ded44738b110c57c51e8478d05efe8a8cd6fcea6f9d9e09dea9e
sui client call --package 0x3 --module sui_system --function report_validator --args 0x5 0x415224057e86d9430e5cb91b98c6c9c10b8595be25b7f755b82d19e6674ec12f 0x92c7bf9914897e8878e559c19a6cffd22e6a569a6dd4d26f8e82e0f2ad1873d6 --gas-budget 20000000 --gas 0x06ddb5d91937ded44738b110c57c51e8478d05efe8a8cd6fcea6f9d9e09dea9e
sui client call --package 0x3 --module sui_system --function report_validator --args 0x5 0x415224057e86d9430e5cb91b98c6c9c10b8595be25b7f755b82d19e6674ec12f 0x054f9044e0fd71c2ff621981c332ba41d686fb705143d1dfd3a3b69a46e8f66e --gas-budget 20000000 --gas 0x06ddb5d91937ded44738b110c57c51e8478d05efe8a8cd6fcea6f9d9e09dea9e

# untally
sui client call --package 0x3 --module sui_system --function undo_report_validator --args 0x5 0x415224057e86d9430e5cb91b98c6c9c10b8595be25b7f755b82d19e6674ec12f 0x3b5664bb0f8bb4a8be77f108180a9603e154711ab866de83c8344ae1f3ed4695 --gas-budget 20000000 --gas 0x06ddb5d91937ded44738b110c57c51e8478d05efe8a8cd6fcea6f9d9e09dea9e
sui client call --package 0x3 --module sui_system --function undo_report_validator --args 0x5 0x415224057e86d9430e5cb91b98c6c9c10b8595be25b7f755b82d19e6674ec12f 0x054f9044e0fd71c2ff621981c332ba41d686fb705143d1dfd3a3b69a46e8f66e --gas-budget 20000000 --gas 0x06ddb5d91937ded44738b110c57c51e8478d05efe8a8cd6fcea6f9d9e09dea9e

# tally cypher
sui client call --package 0x3 --module sui_system --function report_validator --args 0x5 0x62d087c77dba90e5d3fb1f7480f3b3bb1d56e9e7041ae74602f5cec775fad7a6 0x3b5664bb0f8bb4a8be77f108180a9603e154711ab866de83c8344ae1f3ed4695 --gas-budget 20000000 --gas 0x02b89dd33e65e53b86e58539154f8025621618682d22fce1af1390d3e9ee19dc
sui client call --package 0x3 --module sui_system --function report_validator --args 0x5 0x62d087c77dba90e5d3fb1f7480f3b3bb1d56e9e7041ae74602f5cec775fad7a6 0x92c7bf9914897e8878e559c19a6cffd22e6a569a6dd4d26f8e82e0f2ad1873d6 --gas-budget 20000000 --gas 0x02b89dd33e65e53b86e58539154f8025621618682d22fce1af1390d3e9ee19dc
sui client call --package 0x3 --module sui_system --function report_validator --args 0x5 0x62d087c77dba90e5d3fb1f7480f3b3bb1d56e9e7041ae74602f5cec775fad7a6 0x054f9044e0fd71c2ff621981c332ba41d686fb705143d1dfd3a3b69a46e8f66e --gas-budget 20000000 --gas 0x02b89dd33e65e53b86e58539154f8025621618682d22fce1af1390d3e9ee19dc
# untally cypher
sui client call --package 0x3 --module sui_system --function undo_report_validator --args 0x5 0x62d087c77dba90e5d3fb1f7480f3b3bb1d56e9e7041ae74602f5cec775fad7a6 0x3b5664bb0f8bb4a8be77f108180a9603e154711ab866de83c8344ae1f3ed4695 --gas-budget 20000000 --gas 0x02b89dd33e65e53b86e58539154f8025621618682d22fce1af1390d3e9ee19dc
sui client call --package 0x3 --module sui_system --function undo_report_validator --args 0x5 0x62d087c77dba90e5d3fb1f7480f3b3bb1d56e9e7041ae74602f5cec775fad7a6 0x054f9044e0fd71c2ff621981c332ba41d686fb705143d1dfd3a3b69a46e8f66e --gas-budget 20000000 --gas 0x02b89dd33e65e53b86e58539154f8025621618682d22fce1af1390d3e9ee19dc

# indexer
curl --location --request POST 'http://localhost:9200' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "suix_getCoinMetadata",
  "params": [ "0x3dcd4c09250a6c7cc073bab411fccb37934ca754e375a43b8e682ef359e60df::psyop::PSYOP"]
}'
