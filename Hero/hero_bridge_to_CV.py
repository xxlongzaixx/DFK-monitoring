from web3 import Web3
import time
import logging
import sys


private_key = ''
HEROES_ID = [208988,245590,236333,207512,211611,200005,225225,234400,240001,242638,244407] # list of heroes ids

gas_price_gwei = 111
bridge_fees = 0.016
ChainID = 53935
CONTRACT_ADDRESS = '0x573e407Be90a50EAbA28748cbb62Ff9d6038A3e9'
tx_timeout_seconds = 30
rpc_address = 'https://harmony-mainnet.chainstacklabs.com'


ABI = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"heroId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"arrivalChainId","type":"uint256"}],"name":"HeroArrived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"heroId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"arrivalChainId","type":"uint256"}],"name":"HeroSent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_srcChainId","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"_srcAddress","type":"bytes32"}],"name":"SetTrustedRemote","type":"event"},{"inputs":[],"name":"assistingAuction","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_srcAddress","type":"bytes32"},{"internalType":"uint256","name":"_srcChainId","type":"uint256"},{"internalType":"bytes","name":"_message","type":"bytes"},{"internalType":"address","name":"_executor","type":"address"}],"name":"executeMessage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_chainId","type":"uint256"}],"name":"getTrustedRemote","outputs":[{"internalType":"bytes32","name":"trustedRemote","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"heroes","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_messageBus","type":"address"},{"internalType":"address","name":"_heroes","type":"address"},{"internalType":"address","name":"_assistingAuction","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"messageBus","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"msgGasLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_heroId","type":"uint256"},{"internalType":"uint256","name":"_dstChainId","type":"uint256"}],"name":"sendHero","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_assistingAuction","type":"address"}],"name":"setAssistingAuctionAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_messageBus","type":"address"}],"name":"setMessageBus","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_msgGasLimit","type":"uint256"}],"name":"setMsgGasLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_srcChainId","type":"uint256"},{"internalType":"bytes32","name":"_srcAddress","type":"bytes32"}],"name":"setTrustedRemote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"initialLogic","type":"address"},{"internalType":"address","name":"initialAdmin","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"stateMutability":"payable","type":"constructor"}]'


log_format = '%(asctime)s|%(name)s|%(levelname)s: %(message)s'
logger = logging.getLogger("DFK-bridge")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)


w3 = Web3(Web3.HTTPProvider(rpc_address))
account = w3.eth.account.privateKeyToAccount(private_key)
w3.eth.default_account = account.address

contract_address = Web3.toChecksumAddress(CONTRACT_ADDRESS)
contract = w3.eth.contract(contract_address, abi=ABI)


for hero in HEROES_ID:
    nonce = w3.eth.getTransactionCount(account.address)

    tx = contract.functions.sendHero(int(hero), ChainID).buildTransaction(
        {'value': w3.toWei(bridge_fees, 'ether'), 'gasPrice': w3.toWei(gas_price_gwei, 'gwei'), 'nonce': nonce})


    logger.debug("Signing transaction")
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    logger.debug("Sending transaction " + str(tx))
    ret = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logger.debug("Transaction successfully sent !")
    logger.info(
        "Waiting for transaction " + signed_tx.hash.hex() + " to be mined")

    tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash=signed_tx.hash, timeout=tx_timeout_seconds,
                                                     poll_latency=2)
    logger.info("Hero : {} , tx : {}".format(str(hero), tx_receipt))
    logger.info("Transaction mined !")

    time.sleep(5)
