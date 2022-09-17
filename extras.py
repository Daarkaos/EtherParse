import getopt
import os
import sys
from config import InfuraKey
from termcolor import colored

InfuraApi = InfuraKey

# Def for args

def main(argv):
   tx = ''
   web = False
   contract = False
   api = True
   vulns = False
   try:
      opts, args = getopt.getopt(argv,"ht:wcqv",["tx=","web","contract","quiet", "vulns"])
   except getopt.GetoptError:
      print ('parseether.py -tx <hashtx> -w (optional) -c (optional) -q (optional) -v (optional)')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('parseether.py -tx <hashtx> -w (optional) -c (optional) -q (optional) -v (optional)')
         print ('if you want parse data to web server use -w/--web')
         print ('if you want download the contracts use -c/--contract')
         print ('if you want scan the vulnerabilities use -v/--vulns')
         print ('if you do not want to get the data from transaction use -a/--api')
         sys.exit()
      elif opt in ("-t", "--tx"):
         tx = arg
      elif opt in ("-w", "--web"):
         web = True
      elif opt in ("-c", "--contract"):
         contract = True
      elif opt in ("-q", "--quiet"):
         api = False
      elif opt in ("-v", "--vulns"):
         vulns = True
   return (tx, web, contract, api, vulns)


# Study the contracts

def study_contract(to_clean, code_to):
   print(colored('[*] Writting code in Contracts/' + to_clean + '/', 'green'))
   f = open('contracts/' + to_clean + '/' + to_clean + '.bytecode', "w")
   f.write(code_to)
   f.close()
   print (colored('Done *', 'green'))

   print(colored('[*] Doing decompilation', 'green'))

   os.system('panoramix ' + code_to + '> contracts/' + to_clean + '/decompiled_' + to_clean)

   print(colored('[*] Doing static analysis', 'green'))

   os.system('evm-cfg-builder contracts/' + to_clean + '/' + to_clean + '.bytecode --export-dot contracts/' + to_clean)


def mythril_to_contracts(list_of_contracts, hashtx):

   os.system('sudo docker pull mythril/myth > /dev/null')

   for contract in list_of_contracts:

      print(colored('[*] Analyzing ' + contract, 'green'))

      output = os.system('sudo docker run mythril/myth analyze -a ' + contract + ' --execution-timeout 120 --infura-id ' + InfuraApi + ' > contracts/TX-' + hashtx + '/' + contract)

      if output != 0:

         print(colored('VULNERABILITY DETECTED! - ' + contract, 'red'))
      
      else:

         os.remove('contracts/TX-' + hashtx + '/' + contract)



