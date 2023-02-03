import argparse
import csv
from datetime import datetime
from operator import itemgetter


parser = argparse.ArgumentParser(
    prog = "Spendy",
    description = "Tool to parse Lloyds CSV exports and produce insights" )

parser.add_argument("filename")
parser.add_argument("--print", action="store_true")
parser.add_argument("--total_out", action="store_true")
parser.add_argument("--total_in", action="store_true")
parser.add_argument("--start_date", "-s", help="Start date to filter a subset of transactions. Defaults to first transaction if not set. Supply in a valid ISO format")
parser.add_argument("--end_date", "-e", help="End date to filter a subset of transactions. Defaults to last transaction if not set. Supply in a valid ISO format")

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

start = datetime.strptime(args.start_date, "%Y-%m-%d").date() if args.start_date is not None else data[0]["date"]
end = datetime.strptime(args.end_date, "%Y-%m-%d").date() if args.end_date is not None else data[-1]["date"]

txns = [d for d in data if d["date"] >= start and d["date"] <= end]

if args.print:
    for t in txns:
        print_transaction(t)

def total_out():
    out = 0
    for t in txns:
        out = out + t["amount_out"]
    return out

if args.total_out:
    print("Total out: {:.2f}".format(total_out()))

    
