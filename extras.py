import getopt
import os
from termcolor import colored

# Def for args

def main(argv):
   tx = ''
   web = False
   contract = False
   api = True
   try:
      opts, args = getopt.getopt(argv,"ht:wcq",["tx=","web","contract","quiet"])
   except getopt.GetoptError:
      print ('parseether.py -tx <hashtx> -w (optional) -c (optional) -q (optional)')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('parseether.py -tx <hashtx> -w (optional) -c (optional) -q (optional')
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