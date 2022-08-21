<p align="center">
	<img src="/webserver/dist/images/TestTitle.png" height="100px"/>
</p>

Tested with:

Operating System: <b>Ubuntu 22.04 LTS</b>

Python version: <b>Python 3.10.4</b>


## Installation

Before you can start using the program:

You should register on [Etherscan.io](https://etherscan.io/) and [generate an API key](https://etherscan.io/myapikey) to use. 

You should register on [Alchemy.com](https://www.alchemy.com/) and [generate an APP to get the API key](https://dashboard.alchemyapi.io/apps) to use.

Once you have registered and have the necessary API keys, you must download the requirements for this, we will have to use the following steps.

``` bash
git clone https://github.com/Daarkaos/EtherScanParse.git
```

``` bash
pip install requirements.txt
```

## Usage

In `python`, create a client with your personal [Etherscan.io](https://etherscan.io/) and [Alchemy.com](https://www.alchemy.com/) API key:

``` python

apiKey = "YOUR API KEY"  # From Alchemy
eth = Etherscan("YOUR API KEY")  # From Etherscan
```
To execute it:

``` bash
python3 parseether.py --tx 0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530
```

## Examples

``` bash
python3 parseether.py --tx 0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530
```

Output for a complet transaction:

<p align="center">
	<img src="/images/Output1.png" height="50px"/>
</p>


``` bash
python3 parseether.py --tx 0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76531
```

Output for a no valid transaction hash:

<p align="center">
	<img src="/images/Output2.png" height="50px"/>
</p>


``` bash
python3 parseether.py --tx 0x1d2703235da5f5057d1f28fb877924659f1834c049d1fa977aa4a123973a8de3
```

Output for a "small transaction":

<p align="center">
	<img src="/images/Output3.png" height="75px"/>
</p>

## Files

* You can find the json file of the transaction in the path:
``` bash
./json/txhash.json
```
And see some examples [here](json/)


* You can find the contracts downloaded in the path:
``` bash
./contracts/addrhash.bytecode
```
And see some examples [here](contracts/)
