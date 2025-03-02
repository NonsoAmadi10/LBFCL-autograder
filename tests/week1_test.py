import json
from utils import (
    validate_bitcoin_config,
    validate_network_info,
    validate_blockchain_info,
    validate_getinfo,
    validate_wallet_info,
    validate_signet_address,
    validate_transaction,
    validate_raw_transaction,
    validate_segwit_transaction
)

def grade_week1(week_content):
    score = 0
    feedback = []

    # Check bitcoin.conf
    if 'bitcoin.conf' in week_content:
        config = week_content['bitcoin.conf']
        if validate_bitcoin_config(config):
            score += 10
            feedback.append("Bitcoin configuration is correct.")
        else:
            feedback.append("Bitcoin configuration is incorrect or incomplete.")
    else:
        feedback.append("bitcoin.conf file is missing.")

    # Check getnetworkinfo
    if 'getnetworkinfo.json' in week_content:
        try:
            network_info = json.loads(week_content['getnetworkinfo.json'])
            if validate_network_info(network_info):
                score += 10
                feedback.append("getnetworkinfo output is valid.")
            else:
                feedback.append("getnetworkinfo output is invalid or incomplete.")
        except json.JSONDecodeError:
            feedback.append("getnetworkinfo.json is not a valid JSON file.")
    else:
        feedback.append("getnetworkinfo.json file is missing.")

    # Check getblockchaininfo
    if 'getblockchaininfo.json' in week_content:
        try:
            blockchain_info = json.loads(week_content['getblockchaininfo.json'])
            if validate_blockchain_info(blockchain_info):
                score += 10
                feedback.append("getblockchaininfo output is valid.")
            else:
                feedback.append("getblockchaininfo output is invalid or incomplete.")
        except json.JSONDecodeError:
            feedback.append("getblockchaininfo.json is not a valid JSON file.")
    else:
        feedback.append("getblockchaininfo.json file is missing.")

    # Check getinfo
    if 'getinfo.json' in week_content:
        try:
            getinfo = json.loads(week_content['getinfo.json'])
            if validate_getinfo(getinfo):
                score += 10
                feedback.append("getinfo output is valid.")
            else:
                feedback.append("getinfo output is invalid or incomplete.")
        except json.JSONDecodeError:
            feedback.append("getinfo.json is not a valid JSON file.")
    else:
        feedback.append("getinfo.json file is missing.")

    # Check getwalletinfo
    if 'getwalletinfo.json' in week_content:
        try:
            wallet_info = json.loads(week_content['getwalletinfo.json'])
            if validate_wallet_info(wallet_info):
                score += 10
                feedback.append("getwalletinfo output is valid. Wallet creation verified.")
            else:
                feedback.append("getwalletinfo output is invalid or wallet not created.")
        except json.JSONDecodeError:
            feedback.append("getwalletinfo.json is not a valid JSON file.")
    else:
        feedback.append("getwalletinfo.json file is missing.")

    # Check signet address
    if 'signet_address.txt' in week_content:
        address = week_content['signet_address.txt'].strip()
        if validate_signet_address(address):
            score += 10
            feedback.append("Valid signet address created.")
        else:
            feedback.append("Invalid signet address.")
    else:
        feedback.append("signet_address.txt file is missing.")

    # Check simple transaction
    if 'transaction.json' in week_content:
        try:
            transaction = json.loads(week_content['transaction.json'])
            if validate_transaction(transaction):
                score += 10
                feedback.append("Valid simple transaction created.")
            else:
                feedback.append("Invalid or incomplete transaction.")
        except json.JSONDecodeError:
            feedback.append("transaction.json is not a valid JSON file.")
    else:
        feedback.append("transaction.json file is missing.")

    # Check raw transaction
    if 'raw_transaction.txt' in week_content:
        raw_tx = week_content['raw_transaction.txt'].strip()
        if validate_raw_transaction(raw_tx):
            score += 15
            feedback.append("Valid raw transaction on signet network.")
        else:
            feedback.append("Invalid raw transaction or not on signet network.")
    else:
        feedback.append("raw_transaction.txt file is missing.")

    # Check segwit transaction
    if 'segwit_transaction.txt' in week_content:
        segwit_tx = week_content['segwit_transaction.txt'].strip()
        if validate_segwit_transaction(segwit_tx):
            score += 15
            feedback.append("Valid segwit transaction created.")
        else:
            feedback.append("Invalid segwit transaction.")
    else:
        feedback.append("segwit_transaction.txt file is missing.")

    return score, feedback
