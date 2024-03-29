from csv import DictReader
from datetime import date
import os

from ..sources import source


def _parse():
    with open(os.path.join(
        os.path.dirname(__file__), 'data',
        'Average-prices-Property-Type-2018-09.csv',
    )) as f:
        yield from DictReader(f)


MAX_DATE = max((e['Date'] for e in _parse()))


def _build_deck(condition, description_formatter):
    for entry in _parse():
        if not condition(entry):
            continue

        for category_id in ['Detached', 'Semi_Detached', 'Terraced', 'Flat']:
            price_str = entry['{}_Average_Price'.format(category_id)]

            if not price_str:
                continue

            price = float(price_str)

            yield {
                'title': category_id.replace('_', ' '),
                'description': description_formatter(entry),
                'order': price,
                'order_display': '£{:,.2f}'.format(price),
            }


@source('HM Land Registry',
        'House type in UK regions by average price',
        'Cheaper', 'More expensive')
def house_type_and_region_by_average_price():
    yield from _build_deck(
        lambda e: e['Date'] == MAX_DATE, lambda e: e['Region_Name'],
    )


@source('HM Land Registry',
        'House type in UK regions in a given month by average price',
        'Cheaper', 'More expensive')
def house_type_and_region_and_month_by_average_price():
    yield from _build_deck(lambda e: True, lambda e: '{}, {}'.format(
        e['Region_Name'],
        date(*(int(c) for c in e['Date'].split('-')))
        .strftime('%B %Y')
    ))
