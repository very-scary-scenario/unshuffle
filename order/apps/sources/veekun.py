import csv
import os

import pokedex


MONS_CSV = os.path.join(
    os.path.dirname(pokedex.__file__),
    'data', 'csv', 'pokemon.csv',
)


def load():
    ints = {
        'species_id', 'is_default', 'id', 'height', 'base_experience',
        'weight', 'order',
    }

    with open(MONS_CSV) as pf:
        reader = csv.DictReader(pf)
        for mon in reader:
            yield {
                k: int(v) if k in ints else v
                for k, v in mon.items()
            }
