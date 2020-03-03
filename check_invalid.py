import sys
import csv

from tronapi import Tron
from pprint import pprint

tron = Tron()

print("Initiating Script...")
if len(sys.argv)<3:
    print("Please use python check_invalid.py toSend.csv output.csv")
    sys.exit(1)

print("Reading CSV file", sys.argv[1])
print("Saving output to", sys.argv[2])
with open(sys.argv[1], mode='r') as csv_file, open(sys.argv[2], mode='w') as csv_file_out:
    csv_reader = csv.DictReader(csv_file)
    f_names = ['address', 'amount', 'token_name', 'token_ID', 'token_decimals']
    writer = csv.DictWriter(csv_file_out, f_names)
    writer.writeheader()
    line_count = 0
    errors = 0
    for row in csv_reader:
        hex_addr = tron.address.to_hex(row["address"])
        if (hex_addr.find("41",2)>=0):
            writer.writerow({
                'address' : row["address"],
                'amount' : row["amount"],
                'token_name' : row["token_name"],
                'token_ID' : row["token_ID"],
                'token_decimals' : row["token_decimals"],
            })
            print(f'Found error in {row["address"]}')
            errors +=1
        line_count += 1
    print(f'Processed {line_count}. Found {errors} possible fails')

