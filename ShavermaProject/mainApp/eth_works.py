import json
from os import environ
from time import time

from mainApp.environ_vars import key, addr

environ['WEB3_INFURA_PROJECT_ID'] = '3655d24b26c94f948d1937126d38b2eb'

from web3 import Web3, HTTPProvider, eth
from solcx import compile_source

w3 = Web3(HTTPProvider(
    'https://ropsten.infura.io/v3/3655d24b26c94f948d1937126d38b2eb'))

true = True
false = False

stats_address = '0xe4BF2786a3c962760041CD97775e20F038725d29'

ABI_order = [
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "uint128",
                "name": "time",
                "type": "uint128"
            }
        ],
        "name": "set_completed",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_distance_coords",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_status",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [],
        "name": "set_started_delivery",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_info",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            },
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            },
            {
                "internalType": "uint128",
                "name": "",
                "type": "uint128"
            },
            {
                "internalType": "uint128",
                "name": "",
                "type": "uint128"
            },
            {
                "internalType": "uint128",
                "name": "",
                "type": "uint128"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_tx_hash",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "uint8",
                "name": "new_food",
                "type": "uint8"
            }
        ],
        "name": "add_food",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_client",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_food",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_distance",
        "outputs": [
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "string",
                "name": "new_delivery",
                "type": "string"
            },
            {
                "internalType": "uint16",
                "name": "new_dist",
                "type": "uint16"
            }
        ],
        "name": "add_delivery",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "new_client",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "new_tx_hash",
                "type": "string"
            },
            {
                "internalType": "uint128",
                "name": "new_time",
                "type": "uint128"
            },
            {
                "internalType": "string",
                "name": "new_delivery",
                "type": "string"
            },
            {
                "internalType": "uint16",
                "name": "new_dist",
                "type": "uint16"
            },
            {
                "internalType": "uint8",
                "name": "new_food",
                "type": "uint8"
            },
            {
                "internalType": "address",
                "name": "new_restaurant",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    }
]

ABI_stats = [
    {
        "constant": true,
        "inputs": [],
        "name": "get_stats",
        "outputs": [
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            },
            {
                "internalType": "uint256[100]",
                "name": "",
                "type": "uint256[100]"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "",
                "type": "address[]"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get_orders",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "",
                "type": "address[]"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "internalType": "address",
                "name": "order",
                "type": "address"
            }
        ],
        "name": "get_order_info",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "address",
                "name": "order",
                "type": "address"
            },
            {
                "internalType": "uint128",
                "name": "time",
                "type": "uint128"
            }
        ],
        "name": "complete_order",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "address",
                "name": "order",
                "type": "address"
            }
        ],
        "name": "start_delivery",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "internalType": "address",
                "name": "order",
                "type": "address"
            }
        ],
        "name": "add_order",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    }
]
stats_contract = w3.eth.contract(
    address=stats_address,
    abi=ABI_stats
)


def string_to_bytes32(data):
    if len(data) > 32:
        myBytes32 = data[:32]
    else:
        myBytes32 = data.ljust(32, '0')
    return bytes(myBytes32, 'utf-8')


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)


def deploy_contract(contract_interface, coordinates, distance, food, client,
                    transaction, cur_time):
    gas_price = w3.eth.gasPrice * 5
    tx_hash = None
    while True:
        try:
            tx_hash = w3.eth.contract(
                abi=contract_interface['abi'],
                bytecode=contract_interface['bin']).constructor(client,
                                                                transaction,
                                                                cur_time,
                                                                coordinates,
                                                                distance,
                                                                food,
                                                                stats_address).buildTransaction(
                {
                    'chainId': 3,
                    'gasPrice': gas_price,
                    'nonce': w3.eth.getTransactionCount(addr),
                }
            )

            sign_tran = eth.Account.signTransaction(tx_hash, key)
            tx_hash = w3.eth.sendRawTransaction(sign_tran.rawTransaction)
        except ValueError as e:
            gas_price = int(gas_price * 1.4)
            print(e)
        else:
            break
    print('tx_hash', tx_hash)
    address = w3.eth.waitForTransactionReceipt(tx_hash)['contractAddress']
    return address


def add_order(coordinates, distance, food, client, transaction):
    cur_time = int(time())
    food = int(food)
    contract_source_path = 'mainApp/solidity_contracts/order.sol'
    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()
    address = deploy_contract(contract_interface, coordinates, distance, food,
                              client, transaction, cur_time)
    print(address)
    gas_price = w3.eth.gasPrice * 5
    while True:
        try:
            tx_hash = stats_contract.functions.add_order(
                address).buildTransaction(
                {
                    'from': addr,
                    'chainId': 3,
                    'gasPrice': gas_price,
                    'nonce': w3.eth.getTransactionCount(
                        addr),
                    'value': 0

                })
            print(tx_hash)
            sign_tran = eth.Account.signTransaction(tx_hash, key)
            tx_hash = w3.eth.sendRawTransaction(sign_tran.rawTransaction)
            print(sign_tran.rawTransaction)
        except ValueError as e:
            print(e)
            gas_price = int(gas_price * 1.4)
            print(gas_price)
        else:
            w3.eth.waitForTransactionReceipt(tx_hash)
            break

    print('addr', address)
    print(time() - cur_time)
    return address


def get_stats():
    cnt_types_of_food = 8
    stats = stats_contract.functions.get_stats().call()
    mean_dist = stats[0]
    food_choice = stats[1][0:cnt_types_of_food]
    orders_cnt = stats[2]
    completed_orders = stats[3]
    orders = stats[4]
    coords = []
    for item in orders:
        coords.append(stats_contract.functions.get_order_info(item).call()[5])
    return orders_cnt, completed_orders, mean_dist, food_choice, coords


def get_uncompleted_orders():
    stats = stats_contract.functions.get_orders().call()
    undelivered = []
    for order in stats:
        order_contract = w3.eth.contract(
            address=order,
            abi=ABI_order
        )
        if order_contract.functions.get_status().call() == 1:
            undelivered.append(order)
    return undelivered


def change_to_delivery_status(address):
    gas_price = w3.eth.gasPrice * 5
    while True:
        try:
            tx_hash = stats_contract.functions.start_delivery(
                address).buildTransaction(
                {
                    'from': addr,
                    'chainId': 3,
                    'gasPrice': gas_price,
                    'nonce': w3.eth.getTransactionCount(
                        addr),
                    'value': 0

                })
            print(tx_hash)
            sign_tran = eth.Account.signTransaction(tx_hash, key)
            tx_hash = w3.eth.sendRawTransaction(sign_tran.rawTransaction)
            print(sign_tran.rawTransaction)
        except ValueError as e:
            print(e)
            gas_price = int(gas_price * 1.4)
            print(gas_price)
        else:
            w3.eth.waitForTransactionReceipt(tx_hash)
            break


def change_to_completed_status(address, cur_time):
    gas_price = w3.eth.gasPrice * 5
    while True:
        try:
            tx_hash = stats_contract.functions.complete_order(
                address, cur_time).buildTransaction(
                {
                    'from': addr,
                    'chainId': 3,
                    'gasPrice': gas_price,
                    'nonce': w3.eth.getTransactionCount(
                        addr),
                    'value': 0

                })
            print(tx_hash)
            sign_tran = eth.Account.signTransaction(tx_hash, key)
            tx_hash = w3.eth.sendRawTransaction(sign_tran.rawTransaction)
            print(sign_tran.rawTransaction)
        except ValueError as e:
            print(e)
            gas_price = int(gas_price * 1.4)
            print(gas_price)
        else:
            w3.eth.waitForTransactionReceipt(tx_hash)
            break
    order_contract = w3.eth.contract(
        address=address,
        abi=ABI_order
    )
    print(order_contract.functions.get_status().call())


def make_transaction(account, key, value, coordinates, distance, food):
    try:
        signed_txn = w3.eth.account.signTransaction(
            {'from': account,
             'to': addr,
             'chainId': 3,
             'gas': 500000,
             'gasPrice': w3.eth.gasPrice,
             'nonce': w3.eth.getTransactionCount(
                 account),
             'value': w3.toWei(value, 'ether')},
            key)
    except TypeError:
        return 'Wrong key or address'
    try:
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    except ValueError as e:
        error = json.loads(str(e).replace("'", '"'))
        print(error)
        if error['code'] == -32000:
            return 'Not Enough money!'
        else:
            return 'any other problem'
    except:
        return 'any other problem'
    order = add_order(coordinates, distance, food, account, str(tx_hash))
    return tx_hash, order


def get_order_info(addr):
    try:
        callback = stats_contract.functions.get_order_info(addr).call()
    except:
        return 'error'
    else:
        return callback
