# File for functions.
import sys
import re
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

##### Function to get the time from Etherscan transaction
def Get_time_from_tx(EtherHTML):
    parsetime = EtherHTML.find(id="ContentPlaceHolder1_divTimeStamp")
    timestamp = parsetime.find("div", class_="col-md-9")
    timestamp = timestamp.text.replace("\n","")
    timestamp = timestamp[timestamp.find('(')+1:timestamp.find(')')]
    return (timestamp)

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

##### Tokens transfered
def Get_tokens_transfered_from_tx(EtherHTML, internal_tx):
    tokens_transf = []
    tokens = EtherHTML.find_all(id="wrapperContent")
    if tokens:
        #print (len(tokens))
        if len(tokens) >= 2:
                tokens = tokens[1].text
        elif len(tokens) == 1:
            if internal_tx:
                print(colored("NO tokens detected!", "red"))
                return (False)
            else:
                tokens = tokens[0].text
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


def calculate_tokens(web_data):
    
    total_tokens = {}

    for element in web_data['links']:
        
        data_tokens = re.sub("\(.*?\)","",element["value"])
        data_tokens = data_tokens.replace("  "," ")
        data_tokens = data_tokens.split(" ", 1)
        amount = ""
        for m in data_tokens[0]:
            if m.isdigit() or m ==".":
                amount = amount + m
        amount = float(amount)
        name_token = data_tokens[1]

        if element["source"] not in total_tokens:
                total_tokens[element["source"]] = {"received": {}, "send": {}}

        if element["target"] not in total_tokens:
                total_tokens[element["target"]] = {"received": {}, "send": {}}

        # Amount Tokens
        if name_token in (total_tokens[element["source"]]["send"]):
            total_tokens[element["source"]]["send"][name_token] = total_tokens[element["source"]]["send"][name_token] + amount
        else:
            total_tokens[element["source"]]["send"][name_token] = amount
        
        if name_token in (total_tokens[element["target"]]["received"]):
            total_tokens[element["target"]]["received"][name_token] = total_tokens[element["target"]]["received"][name_token] + amount
        else:
            total_tokens[element["target"]]["received"][name_token] = amount
        
    return (total_tokens)

