# MSC
# Import data from Ethereum TX.
import argparse
import colorama
import sys
import json
from config import EtherKey, AlchemyKey
from etherscan import Etherscan
from web3 import Web3, HTTPProvider
from etherscanextractor import *
from termcolor import colored

##### Declare function to define command-line arguments.
def readOptions(args=sys.argv[1:]):
  parser = argparse.ArgumentParser(description="The parsing commands lists.")
  parser.add_argument("-t", "--tx", help="Type the transaction hash.")
  opts = parser.parse_args(args)
  return opts 

# Call functions to read arguments
options = readOptions(sys.argv[1:])
hashtx = sys.argv[2]

#Get data from Web3:
apiKey = AlchemyKey  # From Alchemy
eth = Etherscan(EtherKey)  # From Etherscan
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/'+apiKey))
try:
    transaction = web3.eth.get_transaction(hashtx)
except:
    print(colored('Unable to get information about indicated hash', 'red'))
    print(colored('Check the indicated hash and the API key.', 'red'))
    sys.exit()

print(colored('Getting info about the transaction...', 'green'))
tx_info_clean = {}
tx_info_clean['link'] = "https://etherscan.io/tx/" + hashtx
for element in transaction:
    if element == 'hash':
        value = hashtx
    else:
        value = transaction[element]
    tx_info_clean[element] = value
del tx_info_clean['r']
del tx_info_clean['s']
del tx_info_clean['blockHash']
from_clean = tx_info_clean['from']
to_clean = tx_info_clean['to']

#Execute functions from local file.
EtherHTML = Get_tx_from_etherscan(hashtx = hashtx)
time = Get_time_from_tx(EtherHTML = EtherHTML)
EtherAddrfromHTML = Get_addr_from_etherscan(addrtx = tx_info_clean['from'])
EtherAddrtoHTML = Get_addr_from_etherscan(addrtx = tx_info_clean['to'])
info_addr = Get_info_addr(EtherAddrfromHTML = EtherAddrfromHTML, EtherAddrtoHTML = EtherAddrtoHTML)

# Getting info from internal tx
try:
    tx_internal = eth.get_internal_txs_by_txhash(txhash = hashtx)
    timestamp = tx_internal[0]['timeStamp']
    for element in tx_internal:
        del element['timeStamp']
        del element['blockNumber']
    tx_info_clean['internal_tx'] = tx_internal
    tx_info_clean['timestamp'] = timestamp
except:
    zero = "zero"

#Parse data
tx_info_clean['from'] = info_addr[0]
tx_info_clean['to'] = info_addr[1]
tx_info_clean['time'] = time

# Getting info from tokens transfered
tokens = Get_tokens_transfered_from_tx(EtherHTML = EtherHTML)
tx_info_clean['tokens'] = tokens

# Test if contract exist and write it into a file.
if "Decompile ByteCode" in info_addr[2]:
    EtherHTML_from_contract = Get_contract_from_etherscan(addrcontract = from_clean)
    contract1 = Get_contract_from_addr(EtherContractHTML = EtherHTML_from_contract)
    f = open("webserver/contracts/" + from_clean + ".bytecode", "w")
    f.write(contract1)
    f.close()
    print(colored('CONTRACT \'FROM\' detected, downloading...!', 'green'))

elif "Decompile ByteCode" in info_addr[3]:
    EtherHTML_from_contract = Get_contract_from_etherscan(addrcontract = to_clean)
    contract2 = Get_contract_from_addr(EtherContractHTML = EtherHTML_from_contract)
    f = open("webserver/contracts/" + to_clean + ".bytecode", "w")
    f.write(contract2)
    f.close()
    print(colored('CONTRACT \'TO\' detected, downloading...!', 'green'))

else:
    print(colored('NO contract detected!', 'red'))

#tx_info_clean_json = json.dumps(tx_info_clean)
with open("webserver/json/" + hashtx + '.json', 'w') as json_file:
  json.dump(tx_info_clean, json_file)


test = Transform_data_to_web(tx_info_clean = tx_info_clean)