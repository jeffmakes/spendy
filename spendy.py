import argparse
import csv
from datetime import datetime
from operator import itemgetter


parser = argparse.ArgumentParser(
    prog = "Spendy",
    description = "Tool to parse Lloyds CSV exports and produce insights" )

parser.add_argument("filename")
parser.add_argument("command", choices=['print', 'total_out', 'total_in'])
parser.add_argument("--start_date", "-s", help="Starting date for command that operates on a time period. Supply in a valid ISO format")
parser.add_argument("--end_date", "-e", help="End date for command that operates on a time period. Supply in a valid ISO format")


args = parser.parse_args()
data = []

with open(args.filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=("date", "transaction_type", "sort_code", "account_number", "counterparty", "amount_out", "amount_in", "balance"))
    for row in reader:
        try:
            row["date"] = datetime.strptime(row["date"], "%d/%m/%Y").date()     # Convert date string to date object
            data.append(row)
        except ValueError:
            pass
        
    
for row in data:            # Convert strings to floats, if they're valid
    try:
        row["amount_in"] = float(row["amount_in"])
    except ValueError:
        row["amount_in"] = 0
        pass
    try:
        row["amount_out"] = float(row["amount_out"])
    except ValueError:
        row["amount_out"] = 0
        pass
    try:
        row["balance"] = float(row["balance"])
    except ValueError:
        row["balance"] = 0
        pass

data = sorted(data, key=itemgetter('date'))

def print_transaction(txn):
    print("{}\t{}\t{:20}\t{:.2f}\t{:.2f}\t{:.2f}".format(txn["date"], txn["transaction_type"], txn["counterparty"], txn["amount_out"], txn["amount_in"], txn["balance"]))

if args.command == "print":
    for d in data:
        print_transaction(d)

if args.command == "total_out":
    start = datetime.strptime(args.start_date, "%Y-%m-%d").date()
    end = datetime.strptime(args.end_date, "%Y-%m-%d").date()
    txns = [d for d in data if d["date"] >= start and d["date"] <= end]
    for t in txns:
        print_transaction(t)

    
