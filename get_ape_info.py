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
        headers = {
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_API_SECRET
        }
        metadata_response = requests.get(tokenURI, headers=headers)
        if metadata_response.status_code != 200:
            print(f"Error fetching metadata: HTTP {metadata_response.status_code}")
            return data

        metadata = metadata_response.json()
        print(metadata)

        data['image'] = metadata.get("image", "").replace("ipfs://", f"https://{pinata_gateway}/ipfs/")
        data['eyes'] = next((attr["value"] for attr in metadata.get("attributes", []) if attr["trait_type"] == "eyes"), "")
        data['owner'] = owner
        
    except Exception as e:
        print(f"Error retrieving Ape info: {e}")

    assert isinstance(data, dict), f'get_ape_info({apeID}) should return a dict'
    assert all([a in data.keys() for a in ['owner', 'image', 'eyes']]), "return value should include the keys 'owner', 'image', and 'eyes'"
    return data
