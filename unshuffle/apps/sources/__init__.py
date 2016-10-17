from django.core.cache import cache


SOURCES = {}


def cached(cache_key):
    def wrapper(func):
        def wrapped():
            hit = cache.get(cache_key)

            if hit is None:
                hit = list(func())
                cache.set(cache_key, hit)

            return hit
        return wrapped
    return wrapper


def source(name):
    def _register_source(func):
        func.deck_name = name
        SOURCES[name] = func
        return func

    return _register_source


from ..sources import (  # noqa
    anilist,
    giantbomb,
    veekun,
    wikipedia,
)
