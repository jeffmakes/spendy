import uuid
from itertools import combinations
from thefuzz import fuzz

class Counterparty:
    def __init__(self, name, aliases):
        self.name = name
        self.aliases = aliases
        self.uuid = uuid.uuid1()

def from_transactions(transactions, threshold=60):
    """ Return a set of unique counterparties in a list of transactions """
    
    refs = set()           # use a set type to maintain uniqueness
    for t in transactions:
        refs.add(t.transaction_ref)

    minGroupSize = 1

    paired = { c:{c} for c in refs }
    for a,b in combinations(refs,2):
        if fuzz.partial_ratio(a, b) < threshold: continue
        paired[a].add(b)
        paired[b].add(a)

    groups    = list()
    ungrouped = set(refs)
    while ungrouped:
        bestGroup = {}
        for ref in ungrouped:
            g = paired[ref] & ungrouped
            for c in g.copy():
                g &= paired[c] 
            if len(g) > len(bestGroup):
                bestGroup = g
        if len(bestGroup) < minGroupSize : break  # to terminate grouping early change minGroupSize to 3
        ungrouped -= bestGroup
        groups.append(bestGroup)

    groups_ord = []
    for g in groups:
        groups_ord.append(list(g))

    groups_ord.sort()
    print(groups_ord)

