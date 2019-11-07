import re

from bs4 import BeautifulSoup
from django.core.cache import cache
import requests

from ..sources import source


def _get_article(path):
    path = path.lstrip('/')
    ck = 'smashwiki:{}'.format(path)
    hit = cache.get(ck)

    if hit is not None:
        return hit
    else:
        resp = requests.get('https://www.ssbwiki.com/{}'.format(path))
        resp.raise_for_status()
        cache.set(ck, resp.content)
        return resp.content


def smashwiki_path_soup(path):
    return BeautifulSoup(_get_article(path), 'lxml')


def smashwiki_soup(article):
    soup = smashwiki_path_soup('/{}'.format(article))
    return soup.find(id='bodyContent')


@source('SmashWiki', 'Fighters by weight (SSBU)')
def weight():
    tables = smashwiki_soup('Weight').find_all(class_='wikitable')
    table, = (t for t in tables if t.find(title='Jigglypuff (SSBU)'))
    for row in (r for r in table.find_all('tr') if r.find('td')):
        _, fighter, value = (cell.text.strip() for cell in row.find_all('td'))
        yield {
            'title': fighter,
            'order': int(value),
        }


@source('SmashWiki', 'Fighters by gravity (SSBU)')
def gravity():
    tables = smashwiki_soup('Gravity').find_all(class_='wikitable')
    table, = (t for t in tables if t.find(title='Jigglypuff (SSBU)'))
    for row in (r for r in table.find_all('tr') if r.find('td')):
        _, fighter, value = (cell.text.strip() for cell in row.find_all('td'))
        yield {
            'title': fighter,
            'order': float(value),
        }


@source('SmashWiki', 'Fighters by run speed (SSBU)')
def run_speed():
    tables = smashwiki_soup('Dash').find_all(class_='wikitable')
    table, = (t for t in tables if t.find(title='Jigglypuff (SSBU)'))
    for row in (r for r in table.find_all('tr') if r.find('td')):
        (_, fighter, _, value, *_) = (
            cell.text.strip() for cell in row.find_all('td')
        )
        yield {
            'title': fighter,
            'order': float(value),
        }


@source('SmashWiki', 'Fighters by walk speed (SSBU)')
def walk_speed():
    tables = smashwiki_soup('Walk').find_all(class_='wikitable')
    table, = (t for t in tables if t.find(title='Jigglypuff (SSBU)'))
    for row in (r for r in table.find_all('tr') if r.find('td')):
        (_, fighter, value) = (
            cell.text.strip() for cell in row.find_all('td')
        )
        yield {
            'title': fighter,
            'order': float(value),
        }
