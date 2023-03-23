# get sui validator states
curl --location --request POST 'https://rpc-ws-testnet-w3.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sui_getLatestSuiSystemState",
  "params": [ "0x5"]
}'

# get self stake
curl --location --request POST 'https://rpc-ws-testnet-w3.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
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
sui client merge-coin --primary-coin 0xf3b91028c4cb0a42ae1576b865b183e9d40e4b96314a3d14988182df5e73a3bc --coin-to-merge  0xee967429f74791efac16bb5d11f201a667a035bfbc465e4060775827e99e17e3 --gas-budget 20000000 --gas 0x1830f5cef753277180773be0f29e60a0605b3cc4b87f7f1e4829d355eba24148
sui client merge-coin --primary-coin 0xf3b9...3a3bc --coin-to-merge  0xe6e...0ae --gas-budget 20000000 --gas 0x1830...148


# set gas price
sui client call --package 0x2 --module sui_system --function request_set_gas_price --args 0x5 0xcffcbbf637ac80bfab74fa43b2538ce97109959d49b738929bf9a087b262ca12 900 --gas-budget 20000000 --gas 0x1830f5cef753277180773be0f29e60a0605b3cc4b87f7f1e4829d355eba24148