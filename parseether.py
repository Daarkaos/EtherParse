# MSC
# Import data from Ethereum TX.
import argparse
import getopt
import sys
import json
from config import EtherKey, AlchemyKey
from etherscan import Etherscan
from web3 import Web3, HTTPProvider
from etherscanextractor import *
from termcolor import colored

def main(argv):
   tx = ''
   web = False
   contract = False
   api = True
   try:
      opts, args = getopt.getopt(argv,"ht:wca",["tx=","web","contract","api"])
   except getopt.GetoptError:
      print ('parseether.py -tx <hashtx> -w (optional) -c (optional)')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('parseether.py -tx <hashtx> -w (optional) -c (optional) -a (optional')
         print ('if you want parse data to web server use -w/--web')
         print ('if you want download the contracts use -c/--contract')
         print ('if you dont want to get the data from transacction use -a/--api')
         sys.exit()
      elif opt in ("-t", "--tx"):
         tx = arg
      elif opt in ("-w", "--web"):
         web = True
      elif opt in ("-c", "--contract"):
         contract = True
      elif opt in ("-a", "--api"):
         api = False

   return (tx, web, contract, api)

# Call functions to read arguments

data_arg = main(sys.argv[1:])
hashtx = data_arg[0]

# Get data from Web3:

apiKey = AlchemyKey  # From Alchemy
eth = Etherscan(EtherKey)  # From Etherscan
web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/'+apiKey))
try:
    transaction = web3.eth.get_transaction(hashtx)
except:
    print(colored('Unable to get information about indicated hash', 'red'))
    print(colored('Check the indicated hash and the API key.', 'red'))
    sys.exit()

print(colored('[*] Getting information about the transaction...', 'green'))
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

# Execute functions from local file.

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

# Parse data

tx_info_clean['from'] = info_addr[0]
tx_info_clean['to'] = info_addr[1]
tx_info_clean['time'] = time

# Getting info from tokens transfered

tokens = Get_tokens_transfered_from_tx(EtherHTML = EtherHTML)
tx_info_clean['tokens'] = tokens

# Test if contract exit and download it --- ONLY CONTRACT

if data_arg[2] == True:
    if "Decompile ByteCode" in info_addr[2]:
        EtherHTML_from_contract = Get_contract_from_etherscan(addrcontract = from_clean)
        contract1 = Get_contract_from_addr(EtherContractHTML = EtherHTML_from_contract)
        f = open("contracts/" + from_clean + ".bytecode", "w")
        f.write(contract1)
        f.close()
        print(colored('CONTRACT \'FROM\' detected, downloading...!', 'green'))

    else:
        print(colored('NO contract \'FROM\' detected!', 'red'))

    if "Decompile ByteCode" in info_addr[3]:
        EtherHTML_from_contract = Get_contract_from_etherscan(addrcontract = to_clean)
        contract2 = Get_contract_from_addr(EtherContractHTML = EtherHTML_from_contract)
        f = open("contracts/" + to_clean + ".bytecode", "w")
        f.write(contract2)
        f.close()
        print(colored('CONTRACT \'TO\' detected, downloading...!', 'green'))

    else:
        print(colored('NO contract \'TO\' detected!', 'red'))

#tx_info_clean_json = json.dumps(tx_info_clean)

# Parse data to create graphs --- ONLY WEB.

if data_arg[1] == True:

    print(colored('[*] Starting to parse data to web server...', 'green'))

    web_data = Transform_data_to_web(tx_info_clean = tx_info_clean)

    with open("webserver/json/internaltx/" + hashtx + '.json', 'w') as json_file:
        json.dump(web_data[0], json_file)

    with open("webserver/json/tokens/" + hashtx + '.json', 'w') as json_file:
        json.dump(web_data[1], json_file)
    
    with open("webserver/json/" + hashtx + '.json', 'w') as json_file:
        json.dump(tx_info_clean, json_file)

if data_arg[3] == True:
    tx_info_clean_json = json.dumps(tx_info_clean)
    print (tx_info_clean_json)
        