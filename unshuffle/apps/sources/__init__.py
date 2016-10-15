SOURCES = {}


def source(name):
    def _register_source(func):
        SOURCES[name] = func

    return _register_source


from ..sources import (  # noqa
    veekun,
)
