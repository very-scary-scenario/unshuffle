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


@source('Wikipedia: Hentai anime by the first sentence of their plot '
        '(alphabetical, by title)')
def hentai_by_plot():
    list_soup = wikipedia_soup('List_of_hentai_anime')

    for anchor in list_soup.select(
        '#mw-content-text > ul > li > i > a[title]'
    ):
        title = anchor.get_text()
        soup = wikipedia_path_soup(anchor['href'])
        plot_titles = soup.select('#Plot, #Story')

        if not plot_titles:
            continue

        element = plot_titles[0].parent

        while element is not None and element.name != 'p':
            element = element.next_sibling

        if element is None:
            continue

        for undesired in element.select('sup'):
            undesired.clear()

        plot = truncatechars(element.get_text().replace(title, '[title]'), 140)

        yield {
            'description': plot,
            'order': title,
        }
