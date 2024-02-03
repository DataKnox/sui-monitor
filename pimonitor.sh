#!/bin/bash

# Hosts and their respective ports to check
declare -A hosts=(["69.2.39.166"]="8080 tcp" ["69.2.39.169"]="8080 tcp" ["69.2.39.164"]="8001 udp" ["69.2.39.165"]="8080 tcp" ["69.2.39.167"]="8080 tcp")

# Email settings
recipient_email="your_email@example.com"
subject="Host Alert"

# Telegram settings
telegram_bot_token="6620559877:AAFKhB3-L7n2vJtWr1eZrz_D4vPMpqqpLqE"
telegram_chat_id="1816534827"

# Function to send email
send_email() {
    echo -e "Subject:${subject}\n\n${1}" | ssmtp "${recipient_email}"
}

# Function to send Telegram message
send_telegram() {
    curl -s -X POST "https://api.telegram.org/bot${telegram_bot_token}/sendMessage" -d chat_id="${telegram_chat_id}" -d text="${1}"
}

# Main loop to check hosts and ports
for host in "${!hosts[@]}"; do
    read -r port protocol <<< "${hosts[$host]}"
    echo "Checking $host on port $port over $protocol..."
    
    # Ping test
    ping -c 1 $host > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "$host is down" | send_telegram "$host down" 
        continue
    fi

    # Port check
    if [ "$protocol" == "tcp" ]; then
        nc -zv $host $port > /dev/null 2>&1
    elif [ "$protocol" == "udp" ]; then
        nc -zvu $host $port > /dev/null 2>&1
    else
        echo "Unknown protocol for $host port $port"
        continue
    fi

    if [ $? -ne 0 ]; then
        echo "$host port $port ($protocol) is closed" | send_telegram "$host port $port closed" 
    else
        echo "$host port $port ($protocol) is open"
    fi
done

solana_rpc_endpoint="https://api.mainnet-beta.solana.com"

check_delinquent_validators() {
    local vote_account="juicQdAnksqZ5Yb8NQwCLjLWhykvXGktxnQCDvMe6Nx"
    local response=$(curl -s -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","id":1,"method":"getVoteAccounts"}' $solana_rpc_endpoint)

    if echo "$response" | jq -e ".result.delinquent[] | select(.votePubkey == \"$vote_account\")" > /dev/null; then
        send_telegram "The vote account $vote_account is delinquent."
    else
        echo "The vote account $vote_account is not delinquent."
    fi
}

# Check for delinquent validators
check_delinquent_validators