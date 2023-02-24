class Transaction:
    def __init__(
            self, date, transaction_type, transaction_ref,
            amount_out, amount_in, balance
    ):
        self.date = date
        self.transaction_type = transaction_type
        self.transaction_ref = transaction_ref
        self.amount_out = amount_out
        self.amount_in = amount_in
        self.balance = balance

    def __str__(self):
        return "{}\t{}\t{:20}\t{:.2f}\t{:.2f}\t{:.2f}".format(
            self.date, self.transaction_type, self.transaction_ref,
            self.amount_out, self.amount_in, self.balance
        )


def within_date_range(transactions, start, end):
    """ Given a list of transactions, return the subset between dates two dates
    start, end -- datetime
    """
    return [t for t in transactions if t.date >= start and t.date <= end]
