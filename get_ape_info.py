from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json

# Contract and ABI setup
bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)
with open('/home/codio/workspace/abi.json', 'r') as f:
    abi = json.load(f)

# Connect to an Ethereum node using Alchemy
alchemy_api_key = "SFvU9KC-VwMQ2O84dcM-RmeQQ4hPIXj_"
api_url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api_key}"
provider = HTTPProvider(api_url)
web3 = Web3(provider)
contract = web3.eth.contract(address=contract_address, abi=abi)

# Pinata Credentials
PINATA_API_KEY = "0285a9b49ee24a8aadea"
PINATA_API_SECRET = "cfe47904eb9a5b7fd08417fde78bb19b85d473ce756c3217caabcbb3e9fffac0"
PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIxYjA0OGZmMi0xMWNkLTRhODMtOWQ4NC1lYWZkMGU4YWEzNzIiLCJlbWFpbCI6ImFydHdheW5lQHNlYXMudXBlbm4uZWR1IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjAyODVhOWI0OWVlMjRhOGFhZGVhIiwic2NvcGVkS2V5U2VjcmV0IjoiY2ZlNDc5MDRlYjlhNWI3ZmQwODQxN2ZkZTc4YmIxOWI4NWQ0NzNjZTc1NmMzMjE3Y2FhYmNiYjNlOWZmZmFjMCIsImlhdCI6MTcwNjU3MjkzMX0.JwvOkQtU-vuGPDgHImRqSCyAeDLbfAllSqnSpJCq0a8"
pinata_gateway = "tan-tremendous-wolf-528.mypinata.cloud"

def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID <= 10000, f"{apeID} must be between 1 and 10000"

    data = {'owner': "", 'image': "", 'eyes': ""}
    
    try:
        owner = contract.functions.ownerOf(apeID).call()
        tokenURI = contract.functions.tokenURI(apeID).call()

        if tokenURI.startswith("ipfs://"):
            ipfs_hash = tokenURI.split("ipfs://")[1]
            tokenURI = f"https://{pinata_gateway}/ipfs/{ipfs_hash}"

        headers = {"Authorization": f"Bearer {PINATA_JWT}"}
        metadata_response = requests.get(tokenURI, headers=headers)
        metadata = metadata_response.json()

        data['image'] = metadata.get("image", "").replace("ipfs://", f"https://{pinata_gateway}/ipfs/")
        data['eyes'] = next((attr["value"] for attr in metadata.get("attributes", []) if attr["trait_type"] == "eyes"), "")
        data['owner'] = owner
    except Exception as e:
        print(f"Error retrieving Ape info: {e}")

    assert isinstance(data, dict), f'get_ape_info({apeID}) should return a dict'
    assert all([a in data.keys() for a in ['owner', 'image', 'eyes']]), "return value should include the keys 'owner', 'image', and 'eyes'"
    return data
