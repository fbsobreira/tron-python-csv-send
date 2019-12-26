import sys
import csv

from tronapi import Tron
from pprint import pprint

full_node = 'https://api.trongrid.io'
solidity_node = 'https://api.trongrid.io'
event_server = 'https://api.trongrid.io'

# Define where to send
PK = "YOURPKHERE"

tron = Tron(full_node=full_node,
        solidity_node=solidity_node,
        event_server=event_server)

def checkTrc10(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val

def setTronPK(pk):
    tron.private_key = pk
    tron.default_address = tron.address.from_private_key(pk).base58

print("Initiating Script...")
if len(sys.argv)<2:
    print("Please use python main.py CSVFileName.csv")
    sys.exit(1)

setTronPK(PK)
print("Reading CSV file", sys.argv[1])
with open(sys.argv[1], mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    errors = 0
    for row in csv_reader:
        print(f'\tSending to {row["address"]} {row["amount"]} {row["token_name"]}.')
        if row["token_ID"] == 0:
            try:
                txn = tron.trx.send(row["address"], float(row["amount"]))
                print(f'Sent {row["address"]} {row["amount"]} {row["token_name"]} {txn["transaction"]["txID"]}')
            except:
                print(f'\t\tError: {inst}') 
                print(f'Fail to send {row["address"]} {row["amount"]} {row["token_name"]}')
                errors += 1
        elif checkTrc10(row["token_ID"]):
            try:
                txn = tron.trx.send_token(row["address"], int(float(row["amount"])*pow(10,int(row["token_decimals"]))), row["token_ID"])
                print(f'\tSent {row["address"]} {row["amount"]} {row["token_name"]} {txn["transaction"]["txID"]}')
            except Exception as inst:
                print(f'\t\tError: {inst}') 
                print(f'\t\tFail to send {row["address"]} {row["amount"]} {row["token_name"]}')
                errors += 1
        else:
            try:
                txn = tron.transaction_builder.trigger_smart_contract(
                    contract_address=tron.address.to_hex(row["token_ID"]),
                    function_selector='transfer(address,uint256)',
                    fee_limit=10000000,
                    call_value=0,
                    parameters=[
                        {'type': 'address', 'value': tron.address.to_hex(row["address"])},
                        {'type': 'int256', 'value': int(float(row["amount"])*pow(10,int(row["token_decimals"])))}
                    ]
                )
                print(f'\tSent {row["address"]} {row["amount"]} {row["token_name"]} {txn["transaction"]["txID"]}')
                txResult = tron.trx.sign_and_broadcast(txn['transaction'])
                if (not txResult['result']):
                    raise Exception('Transfer fail...')
            except Exception as inst:
                print(f'\t\tError: {inst}') 
                print(f'\t\tFail to send {row["address"]} {row["amount"]} {row["token_name"]}')
                errors += 1
        line_count += 1
    print(f'Processed {line_count} transfers. {errors} fails')

