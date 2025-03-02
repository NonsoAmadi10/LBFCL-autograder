import json
import os
import difflib
from bitcoinlib.services.services import Service
from bitcoinlib.transactions import Transaction
# Utility functions required in the test folder to grade students
def validate_bitcoin_config(config_data):
    required_settings = [ "rpcuser", "rpcpassword", "signet=1", "datadir", "rpcauth", "server=1", "listen=1" ]
    return all(setting in config_data for setting in required_settings)


def read_file_content(file_path):
    """Read content from various file types."""
    with open(file_path, 'r') as f:
        if file_path.endswith('.json'):
            return json.load(f)
        else:
            return f.read()

def validate_network_info(info):
    required_keys = ['version', 'subversion', 'protocolversion', 'localservices', 'localrelay', 'timeoffset', 'connections', 'networkactive', 'networks', 'relayfee', 'incrementalfee', 'localaddresses', 'warnings']
    return all(key in info for key in required_keys)


def validate_blockchain_info(info):
    required_keys = ['chain', 'blocks', 'headers', 'bestblockhash', 'difficulty', 'mediantime', 'verificationprogress', 'initialblockdownload', 'chainwork', 'size_on_disk', 'pruned', 'softforks', 'warnings']
    return all(key in info for key in required_keys)

def validate_getinfo(info):
    required_keys = ['version', 'blocks', 'headers', 'verificationprogress', 'timeoffset', 'connections', 'proxy', 'difficulty', 'testnet', 'keypoololdest', 'keypoolsize', 'paytxfee', 'relayfee', 'errors']
    return all(key in info for key in required_keys)

def validate_wallet_info(info):
    required_keys = ['walletname', 'walletversion', 'balance', 'unconfirmed_balance', 'immature_balance', 'txcount', 'keypoololdest', 'keypoolsize', 'paytxfee', 'hdseedid', 'private_keys_enabled']
    return all(key in info for key in required_keys)

def validate_signet_address(address):
    return address.startswith('tb1') or address.startswith('2') or address.startswith('m') or address.startswith('n')

def validate_transaction(transaction):
    required_keys = ['txid', 'hash', 'version', 'size', 'vsize', 'weight', 'locktime', 'vin', 'vout']
    return all(key in transaction for key in required_keys)

def validate_raw_transaction(raw_tx):
    rpc_user = os.getenv("BITCOIN_RPC_USER")
    rpc_password = os.getenv("BITCOIN_RPC_PASSWORD")
    rpc_host=os.getenv("BITCOIN_HOST")
    rpc_port=os.getenv("BICTOIN_PORT")

    service = Service(network="signet", providers=[
        {
            'provider': 'bitcoind',
            'url': f'http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}'
        }
    ])

    try: 
        tx = Transaction.parse_hx(raw_tx)
        return service.gettransaction(tx)
    except:
        return False
    

def validate_segwit_transaction(segwit_tx):
    try:
        tx = Transaction.parse_hex(segwit_tx)
        return any( input.witness_type != 'legacy' for input in tx.inputs)
    except:
        return False


def calculate_similarity(text1, text2):
    """Calculate the similarity ratio between two texts."""
    return difflib.SequenceMatcher(None, str(text1), str(text2)).ratio()


def detect_plagiarism(submissions, threshold=0.8):
    """
    Detect potential plagiarism among submissions.
    
    :param submissions: Dict of student submissions
    :param threshold: Similarity threshold to flag as potential plagiarism
    :return: Dict of flagged submissions with their similarity scores
    """
    plagiarism_results = {}
    students = list(submissions.keys())
    
    for i in range(len(students)):
        for j in range(i + 1, len(students)):
            student1 = students[i]
            student2 = students[j]
            similarity = calculate_similarity(
                json.dumps(submissions[student1], sort_keys=True),
                json.dumps(submissions[student2], sort_keys=True)
            )
            if similarity > threshold:
                if student1 not in plagiarism_results:
                    plagiarism_results[student1] = []
                if student2 not in plagiarism_results:
                    plagiarism_results[student2] = []
                plagiarism_results[student1].append((student2, similarity))
                plagiarism_results[student2].append((student1, similarity))
    
    return plagiarism_results