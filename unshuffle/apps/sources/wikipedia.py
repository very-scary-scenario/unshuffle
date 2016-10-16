import re

from bs4 import BeautifulSoup
import requests

from ..sources import source


def wikipedia_soup(article):
    resp = requests.get('https://en.wikipedia.org/wiki/{}'.format(article))
    resp.raise_for_status()
    return BeautifulSoup(resp.content, 'lxml')


@source('Wikipedia: Countries by population')
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
