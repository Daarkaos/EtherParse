# MSC
# Import data from Ethereum TX.
from hashlib import blake2b
from lib2to3.pgen2 import token
import os
import sys
import json
from config import EtherKey, AlchemyKey
from etherscan import Etherscan
from web3 import Web3, HTTPProvider
from etherscanextractor import *
from alchemy_API import *
from extras import *
from termcolor import colored

# Configure the API keys

apiKey = AlchemyKey  # From Alchemy
eth = Etherscan(EtherKey)  # From Etherscan

# Call functions to read arguments

data_arg = main(sys.argv[1:])
hashtx = data_arg[0]

# Get Data from transaction with web3

web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/'+apiKey))
try:
    transaction = web3.eth.get_transaction(hashtx)
except:
    print(colored('Unable to get information about indicated hash', 'red'))
    print(colored('Check the indicated hash and the API key.', 'red'))
    sys.exit()

# Add link from EtherScan to dict 

print(colored('[*] Getting information about the transaction...', 'green'))
tx_info_clean = {}
tx_info_clean['link'] = "https://etherscan.io/tx/" + hashtx

# Select important data from transaction

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

# Getting and parse info from internal tx

internal_tx_valid = False
try:
    tx_internal = eth.get_internal_txs_by_txhash(txhash = hashtx)
    timestamp = tx_internal[0]['timeStamp']
    for element in tx_internal:
        del element['timeStamp']
        del element['blockNumber']
    tx_info_clean['internal_tx'] = tx_internal
    tx_info_clean['timestamp'] = timestamp
    internal_tx_valid = True

except:
    print(colored("NO internal transaction detected!", "red"))
    tx_info_clean['internal_tx'] = False

# Parse data

tx_info_clean['from'] = info_addr[0]
tx_info_clean['to'] = info_addr[1]
tx_info_clean['time'] = time

# Getting info from tokens transferred

tokens = Get_tokens_transfered_from_tx(EtherHTML = EtherHTML, internal_tx = internal_tx_valid)
tx_info_clean['tokens'] = tokens
tokens_valid = tokens

# Test if contract exit 

code_from_valid = False
code_to_valid = False
code_from = eth_getCode(addrtx=from_clean, apiKey=apiKey)

if code_from != "0x":
    code_from_valid = True
    print(colored('CONTRACT \'FROM\' detected!', 'green'))

else:
    print(colored('CONTRACT \'FROM\' NO detected!', 'red'))

code_to = eth_getCode(addrtx=to_clean, apiKey=apiKey)
if code_to != "0x":
    code_to_valid = True
    print(colored('CONTRACT \'TO\' detected!', 'green'))

else:
    print(colored('CONTRACT \'TO\' NO detected!', 'red'))

# Download and "study" the contracts --- ONLY CONTRACT

if data_arg[2] == True:

    if code_from_valid:

        isdir = os.path.isdir("contracts/" + from_clean)

        if not isdir:
            os.mkdir("contracts/" + from_clean)

        study_contract(from_clean = from_clean, code_from = code_from)
    
    if code_to_valid:

        isdir = os.path.isdir("contracts/" + to_clean)
        
        if not isdir:
            os.mkdir("contracts/" + to_clean)

        study_contract(to_clean = to_clean, code_to = code_to)

# Send data to files

print(colored('[*] Starting to parse data to files...', 'green'))

web_data = Transform_data_to_web(tx_info_clean = tx_info_clean)

if internal_tx_valid:
    for element in web_data[0]['links']:

        if int(element['value']) != 0:
            value = int(element['value']) / 1000000000000000000000
            element['value'] = str(value)[0:6] + 'K Ether'

    print(colored('[*] Parsing internal tx...', 'green'))
    with open("webserver/json/internaltx/" + hashtx + '.json', 'w') as json_file:
        json.dump(web_data[0], json_file)

if tokens_valid:

    total_tokens = calculate_tokens(web_data=web_data[1])
    web_data[1]["total_tokens"] = total_tokens
    print(colored('[*] Parsing tokens...', 'green'))
    with open("webserver/json/tokens/" + hashtx + '.json', 'w') as json_file:
        json.dump(web_data[1], json_file)


with open("webserver/json/" + hashtx + '.json', 'w') as json_file:
    json.dump(tx_info_clean, json_file)


#tx_info_clean_json = json.dumps(tx_info_clean)

if data_arg[3] == True:
    tx_info_clean_json = json.dumps(tx_info_clean)
    print (tx_info_clean_json)

#  Detects security vulnerabilities in smart contracts with Mythril ONLY --vulns

if data_arg[4] == True:

    list_of_contracts = []

    if code_from_valid:
        list_of_contracts.append(from_clean.lower())

    if code_to_valid:
        list_of_contracts.append(to_clean.lower())

    if internal_tx_valid:

        for internal in web_data[0]['nodes']:

            internal = internal['id']

            if internal != "" and internal not in list_of_contracts:

                contract = eth_getCode(addrtx=internal, apiKey=apiKey)

                if contract != "0x":
                    list_of_contracts.append(str(internal))

    if tokens_valid:

        for hashtoken in web_data[1]['nodes']:

            hashtoken = hashtoken['id']

            if hashtoken != "" and hashtoken not in list_of_contracts and "0x" in hashtoken:
                
                contract = eth_getCode(addrtx=hashtoken, apiKey=apiKey)

                if contract != "0x":
                    list_of_contracts.append(str(hashtoken))

    isdir = os.path.isdir("contracts/TX-" + hashtx)

    if not isdir:

        os.mkdir("contracts/TX-" + hashtx)

    mythril_to_contracts(list_of_contracts=list_of_contracts, hashtx=hashtx)

# Parse data to create graphs --- ONLY WEB.

if data_arg[1] == True:
    print(colored('[*] Starting the web server...', 'green'))
    
    os.system('python2 webserver/webserver.py')

