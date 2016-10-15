import csv
import os

import pokedex
from ..sources import source


MONS_CSV = os.path.join(
    os.path.dirname(pokedex.__file__),
    'data', 'csv', 'pokemon.csv',
)


def _pokemon():
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


@source('Veekun: Pokémon by name (alphabetical)')
def pokemon_by_name():
    for mon in _pokemon():
        yield {
            'title': mon['identifier'],
            'order': mon['identifier'],
        }


@source('Veekun: Pokémon by national Pokédex number')
def pokemon_by_national_dex():
    for mon in _pokemon():
        yield {
            'title': mon['identifier'],
            'order': mon['species_id'],
        }
