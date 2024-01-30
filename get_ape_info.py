from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json

# Your provided variables
alchemy_api_key = "SFvU9KC-VwMQ2O84dcM-RmeQQ4hPIXj_"
api_url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api_key}"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

# Load ABI
with open('/home/codio/workspace/abi.json', 'r') as f:
    abi = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=abi)

def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID, f"{apeID} must be at least 1"

    data = {'owner': "", 'image': "", 'eyes': ""}
    
    # Get owner of the Ape
    try:
        data['owner'] = contract.functions.ownerOf(apeID).call()
    except Exception as e:
        raise ValueError(f"Error getting owner: {e}")

    # Get token URI and fetch metadata from IPFS
    try:
        token_uri = contract.functions.tokenURI(apeID).call()
        http_uri = token_uri.replace('ipfs://', 'https://ipfs.io/ipfs/')
        
        metadata_response = requests.get(http_uri)
        metadata = metadata_response.json()
        
        data['image'] = metadata['image']
        print(metadata)
        # Assuming 'eyes' is a key in the 'attributes' list
        for attribute in metadata['attributes']:
            if attribute['trait_type'] == 'Eyes':
                data['eyes'] = attribute['value']
                break

    except Exception as e:
        raise ValueError(f"Error fetching metadata: {e}")

    assert isinstance(data, dict), f'get_ape_info{apeID} should return a dict' 
    assert all([a in data.keys() for a in ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner', 'image' and 'eyes'"
    print(data)
    return data
