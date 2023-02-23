import argparse
from datetime import datetime
import calendar

import csvparser
import counterparty

parser = argparse.ArgumentParser(
    prog = "Spendy",
    description = "Tool to parse Lloyds CSV exports and produce insights" )

#parser.add_argument("command", choices=["cluster"])
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

txns = csvparser.parse(args.filename)

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
    subset = transactions.within_date_range(txns, start, end)
else:
    subset = txns

if args.print:
    for t in subset:
        print(t)

def total_out(txns):
    out = 0
    for t in txns:
        out = out + t.amount_out
    return out

def total_in(txns):
    tin = 0
    for t in txns:
        tin = tin + t.amount_in
    return tin

print("From {} to {} Total in {:.2f} Total out {:.2f}".format(start, end, total_in(subset), total_out(subset)))

counterparty.from_transactions(txns)

