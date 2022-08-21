# MSC
# Import data from Ethereum TX.
import argparse
import getopt
import os
import sys
import json
from config import EtherKey, AlchemyKey
from etherscan import Etherscan
from web3 import Web3, HTTPProvider
from etherscanextractor import *
from alchemy_API import *
from termcolor import colored

def main(argv):
   tx = ''
   web = False
   contract = False
   api = True
   try:
      opts, args = getopt.getopt(argv,"ht:wca",["tx=","web","contract","quiet"])
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
      elif opt in ("-q", "--quiet"):
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
    print(colored("NO internal transacction detected!", "red"))
    tx_info_clean['internal_tx'] = False

# Parse data

tx_info_clean['from'] = info_addr[0]
tx_info_clean['to'] = info_addr[1]
tx_info_clean['time'] = time

# Getting info from tokens transfered
tokens_valid = False
tokens = Get_tokens_transfered_from_tx(EtherHTML = EtherHTML)
tx_info_clean['tokens'] = tokens

if tokens == "":
    tokens_valid = True

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

        print(colored('[*] Writting code in Contracts/' + from_clean + '/', 'green'))
        f = open('contracts/' + from_clean + '/' + to_clean + '.bytecode', "w")
        f.write(code_from)
        f.close()
        print (colored('Done *', 'green'))

        print(colored('[*] Doing decompilation', 'green'))

        os.system('panoramix ' + code_from + '> contracts/' + from_clean + '/decompiled_' + from_clean)

        print(colored('[*] Doing static analysis', 'green'))

        os.system('evm-cfg-builder contracts/' + from_clean + '/' + from_clean + '.bytecode --export-dot contracts/' + from_clean)
    
    if code_to_valid:

        isdir = os.path.isdir("contracts/" + to_clean)
        
        if not isdir:
            os.mkdir("contracts/" + to_clean)

        print(colored('[*] Writting code in Contracts/' + to_clean + '/', 'green'))
        f = open('contracts/' + to_clean + '/' + to_clean + '.bytecode', "w")
        f.write(code_to)
        f.close()
        print (colored('Done *', 'green'))

        print(colored('[*] Doing decompilation', 'green'))

        os.system('panoramix ' + code_to + '> contracts/' + to_clean + '/decompiled_' + to_clean)

        print(colored('[*] Doing static analysis', 'green'))

        os.system('evm-cfg-builder contracts/' + to_clean + '/' + to_clean + '.bytecode --export-dot contracts/' + to_clean)

#tx_info_clean_json = json.dumps(tx_info_clean)

if data_arg[3] == True:
    tx_info_clean_json = json.dumps(tx_info_clean)
    print (tx_info_clean_json)

# Parse data to create graphs --- ONLY WEB.

if data_arg[1] == True:

    print(colored('[*] Starting to parse data to web server...', 'green'))

    web_data = Transform_data_to_web(tx_info_clean = tx_info_clean)

    if internal_tx_valid:
        print ('internal detected')
        with open("webserver/json/internaltx/" + hashtx + '.json', 'w') as json_file:
            json.dump(web_data[0], json_file)
    if tokens_valid:
        print ('tokens detected')
        with open("webserver/json/tokens/" + hashtx + '.json', 'w') as json_file:
            json.dump(web_data[1], json_file)
    
    with open("webserver/json/" + hashtx + '.json', 'w') as json_file:
        json.dump(tx_info_clean, json_file)

    print(colored('[*] Starting the web server...', 'green'))
    
    os.system('python2 webserver/webserver.py')

