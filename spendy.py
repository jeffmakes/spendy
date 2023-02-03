import argparse
import csv
from datetime import datetime
from operator import itemgetter
import calendar

parser = argparse.ArgumentParser(
    prog = "Spendy",
    description = "Tool to parse Lloyds CSV exports and produce insights" )

parser.add_argument("filename")
parser.add_argument("--print", action="store_true")
#parser.add_argument("--total_out", action="store_true")
#parser.add_argument("--total_in", action="store_true")
parser.add_argument("--start_date", "-s", help="Start date to filter a subset of transactions. Defaults to first transaction if not set. Supply in a valid ISO format")
parser.add_argument("--end_date", "-e", help="End date to filter a subset of transactions. Defaults to last transaction if not set. Supply in a valid ISO format")
parser.add_argument("--year", help="Select just one year to filter, or the year to accompany a month.")
parser.add_argument("--month", help="Select just one month to filter. Requires --year also to be specified")
parser.add_argument("--months", action="store_true", help="Print all months for the year")

args = parser.parse_args()
data = []

class Transaction:
    def __init__(self, date, transaction_type, counterparty, amount_out, amount_in, balance):
        self.date = date
        self.transaction_type = transaction_type
        self.counterparty = counterparty
        self.amount_out = amount_out
        self.amount_in = amount_in
        self.balance = balance

    def __str__(self):
        return "{}\t{}\t{:20}\t{:.2f}\t{:.2f}\t{:.2f}".format(self.date, self.transaction_type, self.counterparty, self.amount_out, self.amount_in, self.balance)
        

class Transactions:

    def __init__(self, filename):
        self.data = []
        self.transactions = []

        with open(filename, newline='') as csvfile:
            self.reader = csv.DictReader(csvfile, fieldnames=("date", "transaction_type", "sort_code", "account_number", "counterparty", "amount_out", "amount_in", "balance"))
            for row in self.reader:
                try:
                    row["date"] = datetime.strptime(row["date"], "%d/%m/%Y").date()     # Convert date string to date object
                    self.data.append(row)
                except ValueError:
                    pass
    
        for row in self.data:            # Convert strings to floats, if they're valid
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

        self.data = sorted(self.data, key=itemgetter('date'))
        for row in self.data:
            t = Transaction(row["date"], row["transaction_type"], row["counterparty"], row["amount_out"], row["amount_in"], row["balance"])
            self.transactions.append(t)

    def print(self):
        for t in self.transactions:
            print(t)

    def get_all(self):
        return self.transactions

    def get_date_range(self, start, end):
        return [t for t in self.transactions if t.date >= start and t.date <= end]

txns = Transactions(args.filename)


def print_transaction(txn):
    print("{}\t{}\t{:20}\t{:.2f}\t{:.2f}\t{:.2f}".format(txn["date"], txn["transaction_type"], txn["counterparty"], txn["amount_out"], txn["amount_in"], txn["balance"]))

start = None
end = None
# Only year supplied
if args.year and args.month is None:
    start = datetime.strptime("{}-01-01".format(args.year), "%Y-%m-%d").date()  
    end = datetime.strptime("{}-12-31".format(args.year), "%Y-%m-%d").date()  

if args.year and args.month:
    start = datetime.strptime("{}-{}-01".format(args.year, args.month), "%Y-%m-%d").date()  
    end = datetime.strptime("{}-{}-{}".format(args.year, args.month, calendar.monthrange(int(args.year), int(args.month))[1]), "%Y-%m-%d").date()  

# Extract subset of transactions according to date range, using list comprehension
#txns = [d for d in data if d["date"] >= start and d["date"] <= end]
if start and end:
    subset = txns.get_date_range(start, end)

else:
    subset = txns.get_all()

if args.print:
    for t in subset:
        print(t)

exit(0)

def total_out():
    out = 0
    for t in txns:
        out = out + t["amount_out"]
    return out

def total_in():
    tin = 0
    for t in txns:
        tin = tin + t["amount_in"]
    return tin

print("From {} to {} Total in {:.2f} Total out {:.2f}".format(start, end, total_in(), total_out()))


class Counterparties:
    cp = []

    def add(self, name):        # Name is taken directly from the counterparty field in the CSV
        if not name in cp:
            cp.append(name);
        
