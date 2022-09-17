<p align="center">
	<img src="/webserver/dist/images/TestTitle.png" height="150px"/>
</p>

This program allows you to obtain information about the Ethereum transactions that have been carried out, thus minimizing the time spent studying them.

This tool was tested with:

* Operating System: <b>Ubuntu 22.04 LTS</b>

* Python3 version: <b>Python 3.10.4</b>

* Python2 version: <b>Python 2.7.18</b>


## Installation

Before you can start using the program:

You should register on [Etherscan.io](https://etherscan.io/) and [generate an API key](https://etherscan.io/myapikey) to use. 

You should register on [Alchemy.com](https://www.alchemy.com/) and [generate an APP to get the API key](https://dashboard.alchemyapi.io/apps) to use.

Once you have registered and have the necessary API keys, you must download the requirements for this, we will have to use the following steps.

``` bash
git clone https://github.com/Daarkaos/EtherScanParse.git
```

``` bash
pip install -r requirements.txt
```

## Usage

In `Etherparse.py`, you need to configure your [Etherscan.io](https://etherscan.io/) and [Alchemy.com](https://www.alchemy.com/) API key:

``` python

apiKey = "YOUR API KEY"  # From Alchemy
eth = Etherscan("YOUR API KEY")  # From Etherscan
```
In `extras.py`, you need to configure your [Infura.io](https://infura.io/) API key:

To execute it:

``` bash
python3 parseether.py --tx 0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530
```

### Parameters:

* tx &#8594; <b>Required.</b> Use this parameter to indicate the hash of the transaction.
* quiet &#8594; <b>Optional.</b> Use this parameter if you don't want to see the API output
* web &#8594; <b>Optional.</b> Use this parameter to run a web server and get graphic information
* contract &#8594; <b>Optional.</b> Use this parameter to get information about contracts
* vulns &#8594; <b>Optional.</b> Use this to detect security vulnerabilities in smart contracts

## Examples

``` bash
python3 parseether.py --tx 0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530
```

Output:

<p align="center">
	<img src="/webserver/dist/images/example_execution.png" height="165px"/>
</p>

``` bash
python3 etherparse.py --tx 0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530 -q -v
````

Output:

<p align="center">
	<img src="/webserver/dist/images/example_vulns.png" height="350px"/>
</p>

``` bash
python3 parseether.py --tx 0x1d2703235da5f5057d1f28fb877924659f1834c049d1fa977aa4a123973a8de3
```

Output for a "small transaction":

<p align="center">
	<img src="/images/Output3.png" height="75px"/>
</p>



## Files

* You can find the json file of the transaction in the following [path](webserver/json/):
``` bash
.webserver/json/
```

* You can find the outputs of the analyzed contracts in the following [path](contracts/):
``` bash
./contracts/
```
