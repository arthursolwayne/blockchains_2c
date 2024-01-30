from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json

with open('/home/codio/workspace/abi.json', 'r') as f:
    abi = json.load(f)

alchemy_api_key = "SFvU9KC-VwMQ2O84dcM-RmeQQ4hPIXj_"
api_url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api_key}"
provider = HTTPProvider(api_url)
web3 = Web3(provider)
contract_address = Web3.to_checksum_address(bayc_address)
contract = web3.eth.contract(address=contract_address, abi=abi)

# Pinata Gateway
pinata_gateway = "tan-tremendous-wolf-528.mypinata.cloud"

def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID <= 10000, f"{apeID} must be between 1 and 10000"
    data = {'owner': "", 'image': "", 'eyes': ""}
    data['owner'] = contract.functions.ownerOf(apeID).call()
    tokenURI = contract.functions.tokenURI(apeID).call()
    if tokenURI.startswith("ipfs://"):
        tokenURI = tokenURI.replace("ipfs://", f"https://{pinata_gateway}/ipfs/")
    response = requests.get(tokenURI)
    metadata = response.json()
    data['image'] = metadata.get("image", "").replace("ipfs://", f"https://{pinata_gateway}/ipfs/")
    for attribute in metadata.get("attributes", []):
        if attribute["trait_type"] == "eyes":
            data['eyes'] = attribute["value"]
            break

    assert isinstance(data, dict), f'get_ape_info{apeID} should return a dict' 
    assert all([a in data.keys() for a in ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner', 'image', and 'eyes'"
    return data

