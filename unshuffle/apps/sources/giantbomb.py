import random

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests

from django.conf import settings

from ..sources import source as _source

try:
    GIANTBOMB_API_KEY = settings.GIANTBOMB_API_KEY
except AttributeError:
    print('No Giant Bomb API key; video game sources will not be available.')
    GIANTBOMB_API_KEY = None


LIMIT = 100


def source(name):
    if GIANTBOMB_API_KEY is None:
        return lambda f: None
    return _source(name)


def giantbomb(method, **params):
    resp = requests.get(
        'https://www.giantbomb.com/api/{}/'.format(method),
        params={
            'format': 'json',
            'limit': LIMIT,
            'sort': 'id:asc',
            'api_key': GIANTBOMB_API_KEY,
            **params,
        },
        headers={
            'user-agent': 'unshuffle-source-giantbomb/0.0',
        },
    )
    print(resp.content)
    resp.raise_for_status()
    return resp.json()


def build_deck(field):
    seen_ids = set()
    total = giantbomb('games')['number_of_total_results']

    for i in range(3):
        for game in giantbomb(
            'games',
            offset=random.randrange(0, total-LIMIT)
        )['results']:
            if (
                game['id'] in seen_ids or
                not game[field] or

                # and now we have to attempt to filter out games that nobody
                # has heard of
                len(BeautifulSoup(
                    game['description'] or '', 'lxml'
                ).get_text()) < 1000
            ):
                continue

            seen_ids.add(game['id'])
            yield {
                'title': game['name'],
                'secret_description': ', '.join((
                    p['name'] for p in (game['platforms'] or [])
                )),
                'order': game[field],
            }


@source('Giant Bomb: Games by original release date')
def games_by_release_date():
    for card in build_deck('original_release_date'):
        yield {
            **card,
            'order': parse(card['order']).date(),
        }
