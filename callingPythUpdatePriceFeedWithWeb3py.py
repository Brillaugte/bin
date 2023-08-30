from web3 import Web3
from datetime import datetime, timedelta
import requests


def get_vaa_and_publish_time(price_feed_id):
    base_url = "https://xc-testnet.pyth.network"

    # Get the latest price feeds
    endpoint_latest = "api/latest_price_feeds"
    url_latest = f"{base_url}/{endpoint_latest}?ids[]={price_feed_id}"

    response_latest = requests.get(url_latest)
    if response_latest.status_code != 200:
        print(f"Error getting latest price feeds: {response_latest.status_code}")
        return None, None

    latest_data = response_latest.json()
    publish_time = latest_data[0]['ema_price']['publish_time'] # Extracting publish_time

    # Now use the publish_time to get the last VAA
    endpoint_vaa = "api/get_vaa"
    target_chain = "evm" # Replace with the desired target chain
    url_vaa = f"{base_url}/{endpoint_vaa}?id={price_feed_id}&publish_time={publish_time}&target_chain={target_chain}"

    response_vaa = requests.get(url_vaa)
    if response_vaa.status_code != 200:
        print(f"Error getting VAA: {response_vaa.status_code}")
        return None, None

    vaa_data = response_vaa.json()
    return vaa_data['vaa'], publish_time

# Initialize Web3
w3 = Web3(Web3.HTTPProvider('https://polygon-mumbai.infura.io/v3/8be702b6c9fd46c4be89337df571fdbd'))

# Replace with your contract's address and ABI
contract_address = '0xff1a0f4744e8582DF1aE09D5611b887B6a12925C'
contract = w3.eth.contract(address=contract_address, abi=ABI)

# Your private key
private_key = "nope"

# Assume you have a function get_vaa_and_publish_time(price_feed_id)
price_feed_id = '0xca80ba6dc32e08d06f1aa886011eed1d77c77be9eb761cc10d72b7d0a2fd57a6'
vaa, publish_time = get_vaa_and_publish_time(price_feed_id)

# Format vaa
if isinstance(vaa, str):
    vaa = bytes.fromhex(vaa[2:])  # Remove "0x" and convert to bytes
    vaa = "0x" + vaa.hex()  # Convert back to hex string

# Put vaa in a list
vaa_list = [vaa]
print(vaa_list)
# Build the transaction
transaction = contract.functions.updatePriceFeeds(vaa_list).buildTransaction({
    'gas': 2000000,
    'gasPrice': w3.toWei('20', 'gwei'),
    'nonce': w3.eth.getTransactionCount(w3.eth.account.privateKeyToAccount(private_key).address),
    'value': 5,
})

# Sign the transaction
signed_txn = w3.eth.account.signTransaction(transaction, private_key)

# Send the transaction
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Print the transaction hash
print(f'Transaction hash: {txn_hash.hex()}')


