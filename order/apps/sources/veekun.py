import csv
import os

import pokedex


MONS_CSV = os.path.join(
    os.path.dirname(pokedex.__file__),
    'data', 'csv', 'pokemon.csv',
)


def load():
    with open(MONS_CSV) as pf:
        reader = csv.DictReader(pf)
        for mon in reader:
            yield mon
