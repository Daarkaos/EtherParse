import requests
import json

def eth_getCode(addrtx, apiKey):

    url = "https://eth-mainnet.g.alchemy.com/v2/"+apiKey

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "params": [addrtx],
        "method": "eth_getCode"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response = json.loads(response.text)
    response = response['result']

    return (response)
