SOURCES = {}


def source(name):
    def _register_source(func):
        func.deck_name = name
        SOURCES[name] = func

    return _register_source


from ..sources import (  # noqa
    veekun,
)
