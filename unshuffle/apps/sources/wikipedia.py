import re

from bs4 import BeautifulSoup
from django.core.cache import cache
import requests

from ..sources import source


def _get_article(path):
    path = path.lstrip('/')
    ck = 'wikipedia:{}'.format(path)
    hit = cache.get(ck)

    if hit is not None:
        return hit
    else:
        resp = requests.get('https://en.wikipedia.org/{}'.format(path))
        resp.raise_for_status()
        cache.set(ck, resp.content)
        return resp.content


def wikipedia_path_soup(path):
    return BeautifulSoup(_get_article(path), 'lxml')


def wikipedia_soup(article):
    return wikipedia_path_soup('/wiki/{}'.format(article))


def _country_mcdonalds():
    soup = wikipedia_soup('List_of_countries_with_McDonald%27s_restaurants')

    current_table = soup.select('.wikitable')[0]
    for row in current_table.select('tr'):
        cells = row.select('td')
        if not cells:
            continue
        country, date, first, count, source, people_per_outlet, ref = (
            element.get_text() for element in cells
        )

        if not count.strip():
            continue

        if not people_per_outlet.strip():
            continue

        yield (
            re.sub(r'\(.*\)', '', country).strip(' \n\xa0'),
            int(re.sub(r'(\[\d+\]|,|\+)', '', count)),
            int(re.sub(r'(\[\d+\]|,)', '', people_per_outlet)),
        )


@source('Wikipedia', 'Countries by population')
def countries_by_population():
    soup = wikipedia_soup('List_of_countries_and_dependencies_by_population')

    for row in soup.select('.wikitable tr')[1:]:
        rank, country, population, date, percent, source = (
            element.get_text() for element in row.select('td')
        )
        yield {
            'title': re.sub(r'\[[^\[]+\]', '', country),
            'order': int(population.replace(',', '')),
            'order_display': population,
        }


@source('Wikipedia', "Countries by number of McDonald's outlets")
def countries_by_mcdonalds():
    for country, count, people_per_outlet in _country_mcdonalds():
        yield {
            'title': country,
            'order': count,
            'order_display': '{:,} outlets'.format(count),
        }


@source('Wikipedia', "Countries by number of McDonald's outlets per person")
def countries_by_mcdonalds_per_person():
    for country, count, people_per_outlet in _country_mcdonalds():
        yield {
            'title': country,
            'order': 1/people_per_outlet,
            'order_display': 'one outlet for every {:,} people'
            .format(people_per_outlet),
        }


@source('Wikipedia', 'Languages by number of speakers')
def languages_by_speakers():
    soup = wikipedia_soup('List_of_languages_by_number_of_native_speakers')

    for row in soup.select('.wikitable tr'):
        if row.select('th'):
            continue

        rank, language, millions, percent = (
            element.get_text() for element in row.select('td')
        )
        millions_string = re.sub(r'\(\d+\)|\[.*\]', '', millions).strip()
        millions_count = float(millions_string)
        yield {
            'title': re.sub(r'\[[^\[]+\]', '', language),
            'order': millions_count,
            'order_display': '{} million'.format(millions_string),
        }


@source('Wikipedia', 'Elements by atomic number')
def elements_by_atomic_number():
    soup = wikipedia_soup('List_of_chemical_elements')

    for row in soup.select('.wikitable tr'):
        if row.select('th') or len(row.select('td')) < 10:
            continue

        number, symbol, name, *_ = (
            element.get_text() for element in row.select('td')
        )

        yield {
            'title': '{} ({})'.format(name, symbol),
            'order': int(number),
        }


@source('Wikipedia', 'Restaurant chains by number of locations worldwide')
def restaurant_chains_by_count():
    soup = wikipedia_soup('List_of_restaurant_chains')

    for row in soup.select('.wikitable tr'):
        if row.select('th'):
            continue

        name, _, _, _, _, count_text, *_ = (
            element.get_text() for element in row.select('td')
        )

        try:
            count = int(count_text.replace(',', ''))
        except ValueError:
            continue

        yield {
            'title': name,
            'order': count,
            'order_display': '{:,}'.format(count),
        }


@source('Wikipedia', 'Countries by electricity consumption per person')
def countries_by_energy_consumption_per_capita():
    soup = wikipedia_soup('List_of_countries_by_electricity_consumption')

    for row in soup.select('.wikitable tr'):
        if row.select('th'):
            continue

        rank_cell, country_cell, _, _, _, _, _, _, power_cell = (
            element.get_text() for element in row.select('td')
        )

        try:
            power = int(power_cell.replace(',', ''))
            int(rank_cell)
        except ValueError:
            continue

        yield {
            'title': country_cell.strip(' \n\xa0'),
            'order': power,
            'order_display': '{:,} watts per person'.format(power),
        }
