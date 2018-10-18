import re

from bs4 import BeautifulSoup
from django.template.defaultfilters import truncatechars
import requests

from ..sources import source


def wikipedia_path_soup(path):
    resp = requests.get('https://en.wikipedia.org/{}'.format(path.lstrip('/')))
    resp.raise_for_status()
    return BeautifulSoup(resp.content, 'lxml')


def wikipedia_soup(article):
    return wikipedia_path_soup('/wiki/{}'.format(article))


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


@source('Wikipedia', 'Languages by number of speakers')
def countries_by_population():
    soup = wikipedia_soup('List_of_languages_by_number_of_native_speakers')

    for row in soup.select('.wikitable tr')[1:]:
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
