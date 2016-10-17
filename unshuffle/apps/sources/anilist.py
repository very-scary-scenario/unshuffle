from datetime import datetime

import requests

from django.core.cache import cache
from django.conf import settings

from ..sources import source


AUTH_PARAMS = {}
URL_FMT = 'https://anilist.co/api/{}'
SEASONS = ['winter', 'spring', 'summer', 'fall']
SEASON_CACHE_KEY = 'anilist_seasons'


def _anilist(method, **params):
    return requests.get(
        URL_FMT.format(method),
        params={
            **AUTH_PARAMS,
            **params,
        },
    )


def anilist(*a, **k):
    resp = _anilist(*a, **k)

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        new_token_resp = requests.post(
            URL_FMT.format('auth/access_token'),
            data={
                'grant_type': 'client_credentials',
                'client_id': settings.ANILIST_CLIENT_ID,
                'client_secret': settings.ANILIST_CLIENT_SECRET,
            }
        )
        new_token_resp.raise_for_status()
        AUTH_PARAMS['access_token'] = new_token_resp.json()['access_token']

        try:
            resp = _anilist(*a, **k)
        except requests.exceptions.HTTPError:
            raise RuntimeError(resp.json())

    return resp.json()


def populate_season_cache():
    cards = []

    for year in range(1995, datetime.now().year):
        for season_index, season in enumerate(SEASONS):
            for anime in anilist(
                'browse/anime',
                year=year,
                seaon=season,
                sort='popularity-desc',
            ):
                cards.append({
                    'title': anime['title_english'],
                    'description': ', '.join(anime['genres']),
                    'order': '{}-{}'.format(year, season_index),
                    'order_display': '{} {}'.format(
                        season.capitalize(), year,
                    ),
                })

    cache.set(SEASON_CACHE_KEY, cards)
    return cards


@source('Anilist: Anime by season')
def anime_by_season():
    cards = cache.get(SEASON_CACHE_KEY)

    if cards is None:
        cards = populate_season_cache()

    return cards


# anime_by_season()  # just to populate the cache if it's not populated
