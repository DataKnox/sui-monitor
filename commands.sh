
curl --location --request POST 'https://rpc-ws-testnet-w3.suiscan.xyz:443' --header 'Content-Type: application/json' --data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sui_getLatestSuiSystemState",
  "params": [ "0x5"]
}'

sui client call --package 0x2 --module sui_system --function request_set_commission_rate --args 0x5 1500 --gas-budget 20000000


sui client gas
sui client merge-coin --primary-coin <target> coin-to-merge <source> --gas-budget 20_000_000 --gas <gas object paying for gas>
sui client merge-coin --primary-coin 0xf3b91028c4cb0a42ae1576b865b183e9d40e4b96314a3d14988182df5e73a3bc --coin-to-merge 0xe6e217c923ece3d108fd574d16d6e5a0