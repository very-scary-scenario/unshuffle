from typing import List, Dict

import requests
from django.core.cache import cache

from ..sources import source, cached


URL = 'https://graphql.anilist.co'
SEASONS = ['winter', 'spring', 'summer', 'fall']
POPULAR_ANIME: List[Dict] = []


def _popular_anime(*a, **k):
    ck = 'anilist:popular'
    hit = cache.get(ck)
    if hit:
        yield from hit
    else:
        for page in range(1, 20):
            resp = requests.post(URL, json={
                'query': """
                query ($page: Int) {
                    Page (perPage: 50, page: $page) {
                        pageInfo {
                            hasNextPage
                        }
                        media (type: ANIME, popularity_greater: 20000) {
                            title {
                                romaji
                                english
                            }
                            startDate {
                                year
                            }
                            genres
                            averageScore
                        }
                    }
                }
                """,
                'variables': {'page': page},
            }).json()
            yield from resp['data']['Page']['media']
            if not resp['data']['Page']['pageInfo']['hasNextPage']:
                break


def popular_anime():
    if POPULAR_ANIME:
        yield from POPULAR_ANIME
    else:
        for anime in _popular_anime():
            POPULAR_ANIME.append(anime)
            yield anime


def anime_description(anime):
    return '\n\n'.join((
        anime['title']['romaji']
        if (
            anime['title']['english'] and
            (anime['title']['romaji'] != anime['title']['english'])
        )
        else '',

        ', '.join(anime['genres'])
    ))


@source('Anilist', 'Anime by year', 'Older', 'Newer')
@cached('anilist_seasons')
def anime_by_season():
    for anime in popular_anime():
        yield {
            'title': anime['title']['english'] or anime['title']['romaji'],
            'description': anime_description(anime),
            'order': anime['startDate']['year']
        }


@source('Anilist', 'Anime by user rating', 'Lower rating', 'Higher rating')
@cached('anilist_ratings')
def anime_by_user_rating():
    for anime in popular_anime():
        yield {
            'title': anime['title']['english'],
            'description': (
                anime_description(anime) +
                '\n\n{}'.format(anime['startDate']['year'])
            ),
            'order': anime['averageScore']
        }
