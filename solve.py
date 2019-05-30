#!/usr/bin/env python3

"""Attempt to form a governement after the 2019 Belgian federal elections.

Given the elected parties and constraints like their respective number of seats,
their known restrictions to form a government with certain other parties,
and the will to keep a balance in the FR/NL repartition,
this program will try and display all possible valid combinations.

https://en.wikipedia.org/wiki/2019_Belgian_federal_election
"""

from itertools import combinations
from collections import namedtuple
import math

class Party(namedtuple('Party', ['name', 'seats', 'group'])):
    __slots__ = ()
    def __repr__(self):
        return f"{self.name} ({self.seats})"


parties = [
    Party('N-VA', 25, 'nl'),
    Party('VB', 18, 'nl'),
    Party('PS', 20, 'fr'),
    Party('CD&V', 12, 'nl'),
    Party('PVDA+/PTB', 12, None),    # Seen as both nl and fr
    Party('Open Vld', 12, 'nl'),
    Party('MR', 14, 'fr'),
    Party('sp.a', 9, 'nl'),
    Party('ECOLO', 13, 'fr'),
    Party('Groen', 8, 'nl'),
    Party('cdH', 5, 'fr'),
    Party('DéFI', 2, 'fr'),
]

# Some parties will not accept to form a government with others.
# This list is certainly incomplete.
# https://www.rtbf.be/info/belgique/detail_apres-les-elections-quelle-coalition-pour-la-belgique?id=10232502
exclusions = [
    ('PVDA+/PTB', 'MR'),
    ('PVDA+/PTB', 'cdH'),
    ('MR', 'PVDA+/PTB'),
    # No FR party will accept VB (except maybe DéFI?)
    ('PVDA+/PTB', 'VB'),
    ('PS', 'VB'),
    ('MR', 'VB'),
    ('ECOLO', 'VB'),
    ('cdH', 'VB'),
    ('PS', 'N-VA'),
    # FR parties won't accept N-VA except MR
    ('PVDA+/PTB', 'N-VA'),
    ('PS', 'N-VA'),
    ('MR', 'N-VA'),
    ('ECOLO', 'N-VA'),
    ('cdH', 'N-VA'),
]


def compatible(p1, p2):
    return (p1, p2) not in exclusions and (p2, p1) not in exclusions


def contains_exclusions(government):
    for pair in combinations([p.name for p in government], 2):
        if not compatible(pair[0], pair[1]):
            return True
    return False


def is_linguisticly_balanced(government):
    max_fr_proportion = 0.5
    max_nl_proportion = 0.6
    count_group = lambda lang: sum(p.seats for p in government if p.group == lang)
    # subtract linguisticly "neutral" parties from seat count
    seats = seats_count(government) - count_group(None)
    return count_group('fr') <= max_fr_proportion*seats and count_group('nl') <= max_nl_proportion*seats


def seats_count(government):
    return sum(p.seats for p in government)


if __name__ == "__main__":
    majority = math.ceil(float(sum(p.seats for p in parties) / 2))
    for number_of_parties in range(1, len(parties)+1):
        for government in combinations(parties, number_of_parties):
            seats = seats_count(government)
            if seats >= majority and not contains_exclusions(government) and is_linguisticly_balanced(government):
                    print(f"Government with {number_of_parties} parties and {seats} seats: {government}")
