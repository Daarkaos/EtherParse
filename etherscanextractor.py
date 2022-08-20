# File for functions.
import sys
import requests
from bs4 import BeautifulSoup
from termcolor import colored

##### Function to get the transaction from Etherscan
def Get_tx_from_etherscan(hashtx):
    url = "https://etherscan.io/tx/" + hashtx
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get (url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    if soup.title.string == "Etherscan Error Page":
        print(colored("Could not connect to Etherscan", "red"))
        sys.exit()
    print(colored("[*] Getting information from Etherscan...", "green"))
    return soup

##### Get addr from Etherscan
def Get_addr_from_etherscan(addrtx):
    url = "https://etherscan.io/address/" + addrtx
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get (url, headers=headers)
    soupaddr = BeautifulSoup(page.content, "html.parser")
    return soupaddr

##### Get contract from Etherscan
def Get_contract_from_etherscan(addrcontract):
    url = "https://etherscan.io/bytecode-decompiler?a=" + addrcontract
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get (url, headers=headers)
    soupcontract = BeautifulSoup(page.content, "html.parser")
    return soupcontract

##### Function to get the time from Etherscan transaction
def Get_time_from_tx(EtherHTML):
    parsetime = EtherHTML.find(id="ContentPlaceHolder1_divTimeStamp")
    timestamp = parsetime.find("div", class_="col-md-9")
    timestamp = timestamp.text.replace("\n","")
    timestamp = timestamp[timestamp.find('(')+1:timestamp.find(')')]
    return (timestamp)

##### Function to get the from from Etherscan transaction
#def Get_participants_from_tx(EtherHTML):
#    fromtx = EtherHTML.find(id="spanFromAdd")
#    totx = EtherHTML.find(id="contractCopy")
#    return (fromtx.text, totx.text)

##### Get info from addr
def Get_info_addr(EtherAddrfromHTML, EtherAddrtoHTML):
    type_addr_from = EtherAddrfromHTML.title.string
    type_addr_from = type_addr_from.replace("| Etherscan","").replace("  "," ").replace("\n","").replace("\r","").replace("\t","").replace("Address ","").replace("| ","")
    type_addr_from = type_addr_from.rstrip(type_addr_from[-1])
    type_addr_to = EtherAddrtoHTML.title.string
    type_addr_to = type_addr_to.replace("| Etherscan","").replace("  "," ").replace("\n","").replace("\r","").replace("\t","").replace("Address ","").replace("| ","")
    type_addr_to = type_addr_to.rstrip(type_addr_to[-1])
    type_addr_from_contract = EtherAddrfromHTML.find(id="code").text
    type_addr_to_contract = EtherAddrtoHTML.find(id="code").text
    return (type_addr_from, type_addr_to, type_addr_from_contract, type_addr_to_contract)

##### Import contract
def Get_contract_from_addr(EtherContractHTML):
    contract = EtherContractHTML.find(id="ContentPlaceHolder1_txtByteCode").text
    return (contract)

##### Tokens transfered
def Get_tokens_transfered_from_tx(EtherHTML):
    tokens_transf = []
    tokens = EtherHTML.find_all(id="wrapperContent")
    if tokens:
        if len(tokens) == 2:   
            tokens = tokens[1].text
        else:
            tokens = tokens[0].text
    else:
        print(colored("NO tokens detected!", "red"))
        return (False)
    tokens = tokens.replace("To"," To=").replace("From",";From=").replace("For","For=").split(";")
    for token in tokens:
        token_from = token[token.find('From=')+6:token.find('To=')]
        token_to = token[token.find('To=')+4:token.find('For=')]
        token_for = token[token.find('For=')+5:]
        dict_tokens = {"from": token_from, "to": token_to, "for": token_for}
        tokens_transf.append(dict_tokens)

    del tokens_transf[0]
    return (tokens_transf)

##### Create json to Web
def Transform_data_to_web(tx_info_clean):
    internal = {}
    list_nodes_internal = []
    list_links_internal = []
    tokens = {}
    list_nodes_tokens = []
    list_links_tokens = []
    if tx_info_clean['internal_tx'] != False:
        
        for element in tx_info_clean['internal_tx']:
            added = False
            for p in list_nodes_internal:
                if (p["id"] == element["from"]):
                    added = True
            if not added:
                new_node = { "id": element["from"]}
                list_nodes_internal.append(new_node)
            added = False    
            for p in list_nodes_internal:  
                if (p["id"] == element["to"]):
                    added = True
            if not added:
                new_node = { "id": element["to"]}
                list_nodes_internal.append(new_node)

            new_link = {"source": element['from'], "target": element['to'], "value": element['value']}
            list_links_internal.append(new_link)

        internal["nodes"] = list_nodes_internal
        internal["links"] = list_links_internal

    if tx_info_clean['tokens'] != False:
        
        for element in tx_info_clean['tokens']:
            added = False
            for p in list_nodes_tokens:
                if (p["id"] == element["from"]):
                    added = True
            if not added:
                new_node = { "id": element["from"]}
                list_nodes_tokens.append(new_node)
            added = False    
            for p in list_nodes_tokens:  
                if (p["id"] == element["to"]):
                    added = True
            if not added:
                new_node = { "id": element["to"]}
                list_nodes_tokens.append(new_node)

            new_link = {"source": element['from'], "target": element['to'], "value": element['for']}
            list_links_tokens.append(new_link)

        tokens["nodes"] = list_nodes_tokens
        tokens["links"] = list_links_tokens

    return (internal, tokens)