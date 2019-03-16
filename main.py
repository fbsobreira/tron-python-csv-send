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
        if row["token_name"] == "TRX":
            try:
                txn = tron.trx.send(row["address"], float(row["amount"]))
                print(f'Sent {row["address"]} {row["amount"]} {row["token_name"]} {txn["transaction"]["txID"]}')
            except:
                print(f'\t\tError: {inst}') 
                print(f'Fail to send {row["address"]} {row["amount"]} {row["token_name"]}')
                errors += 1
        else:
            try:
                #print(int(int(row["amount"])*pow(10,int(row["token_decimals"]) ))  )
                txn = tron.trx.send_token(row["address"], int(int(row["amount"])*pow(10,int(row["token_decimals"]))), row["token_ID"])
                print(f'\tSent {row["address"]} {row["amount"]} {row["token_name"]} {txn["transaction"]["txID"]}')
            except Exception as inst:
                print(f'\t\tError: {inst}') 
                print(f'\t\tFail to send {row["address"]} {row["amount"]} {row["token_name"]}')
                errors += 1
        line_count += 1
    print(f'Processed {line_count} transfers. {errors} fails')

