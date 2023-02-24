from transaction import Transaction
import csv
from datetime import datetime
from operator import itemgetter


def parse(filename):
    """ Parse a CSV file and return a list of transactions it contains """

    data = []
    transactions = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(
            csvfile,
            fieldnames=(
                "date", "transaction_type", "sort_code", "account_number",
                "counterparty", "amount_out", "amount_in", "balance"
            )
        )
        for row in reader:
            try:
                # Convert date string to date object
                row["date"] = datetime.strptime(row["date"], "%d/%m/%Y").date()
                data.append(row)
            except ValueError:
                pass

    for row in data:      # Convert strings to floats, if they're valid
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
    for row in data:
        t = Transaction(
            row["date"], row["transaction_type"], row["counterparty"],
            row["amount_out"], row["amount_in"], row["balance"]
        )
        transactions.append(t)

    return transactions
