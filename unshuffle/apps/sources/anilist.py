from datetime import datetime

import requests

from django.conf import settings

from ..sources import source, cached


AUTH_PARAMS = {}
URL_FMT = 'https://anilist.co/api/{}'
SEASONS = ['winter', 'spring', 'summer', 'fall']


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


def anime_description(anime):
    return '\n\n'.join((
        anime['title_romaji']
        if anime['title_romaji'] != anime['title_english']
        else '',

        ', '.join(anime['genres'])
    ))


@source('Anilist', 'Anime by season', 'Older', 'Newer')
@cached('anilist_seasons')
def anime_by_season():
    for year in range(1995, datetime.now().year):
        for season_index, season in enumerate(SEASONS):
            for anime in anilist(
                'browse/anime',
                year=year,
                seaon=season,
                sort='popularity-desc',
            ):
                yield {
                    'title': anime['title_english'],
                    'description': anime_description(anime),
                    'order': '{}-{}'.format(year, season_index),
                    'order_display': '{} {}'.format(
                        season.capitalize(), year,
                    ),
                }


@source('Anilist', 'Anime by user rating', 'Lower rating', 'Higher rating')
@cached('anilist_ratings')
def anime_by_user_rating():
    seen = set()

    for page in range(1, 15):
        for anime in anilist(
            'browse/anime',
            sort='popularity-desc',
            page=page,
        ):
            if anime['id'] in seen:
                raise ValueError(anime)

            seen.add(anime['id'])

            yield {
                'title': anime['title_english'],
                'description': anime_description(anime),
                'order': anime['average_score'],
                'order_display': '{:.2f}%'.format(anime['average_score']),
            }


# anime_by_season()  # just to populate the cache if it's not populated
