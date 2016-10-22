import csv
import os

import pokedex
from ..sources import source


NAMES_CSV = os.path.join(
    os.path.dirname(pokedex.__file__),
    'data', 'csv', 'pokemon_species_names.csv',
)


def _pokemon():
    ints = {
        'pokemon_species_id', 'local_language_id',
    }

    with open(NAMES_CSV) as pf:
        reader = csv.DictReader(pf)
        for mon in reader:
            yield {
                k: int(v) if k in ints else v
                for k, v in mon.items()
            }


def _english_pokemon():
    for mon in _pokemon():
        if mon['local_language_id'] == 9:
            yield mon


@source('Veekun', 'Pokémon by name (alphabetical)')
def pokemon_by_name():
    for mon in _english_pokemon():
        yield {
            'title': mon['name'],
            'order': mon['name'],
        }


@source('Veekun', 'Pokémon by national Pokédex number')
def pokemon_by_national_dex():
    for mon in _english_pokemon():
        yield {
            'title': mon['name'],
            'order': mon['pokemon_species_id'],
            'order_display': '#{}'.format(mon['pokemon_species_id']),
        }


@source('Veekun', 'Pokémon by genus (alphabetical)')
def pokemon_by_genus():
    for mon in _english_pokemon():
        yield {
            'title': mon['name'],
            'order': '{} Pokémon'.format(mon['genus']),
        }
