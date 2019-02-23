import csv
import os
import re

from ..sources import source


def _pluralise(fmt, number):
    return fmt.format(number, '' if number == 1 else 's')


def _parse():
    in_content = False

    for row in csv.reader(open(os.path.join(
        os.path.dirname(__file__),
        'data', 'count-notifiable-offences-nov-2018.csv',
    ))):
        if row[0] == 'Home Office code':
            in_content = True
            continue

        if not in_content:
            continue

        yield row[:13]


ENTRIES = list(_parse())


@source(
    'Home Office', 'Offences by maximum sentence (cw: specific descriptions '
    'of assault)',
)
def offences_by_maximum_sentence():
    for (
        code, _, csv_max_sentence, _, _, _, category, offence, act, *_,
    ) in ENTRIES:

        max_sentence_display = csv_max_sentence
        msd_proc = csv_max_sentence.lower().strip()

        if msd_proc in ('', '?', '-', 'imp'):
            continue

        elif msd_proc in ('life', 'indefinite'):
            max_sentence = 1000
            max_sentence_display = msd_proc.capitalize()
        elif msd_proc == 'unlimited fine':
            max_sentence = 0.002
            max_sentence_display = 'An unlimited fine'
        elif msd_proc == 'fine':
            max_sentence = 0.001
            max_sentence_display = 'A fine'
        elif msd_proc == '2 years/and or fine':
            max_sentence = 2.001
            max_sentence_display = '2 years and/or fine'
        elif re.match(r'\d+ weeks', msd_proc):
            max_sentence = int(msd_proc[:-6]) / 52
        elif re.match(r'\d+m', msd_proc):
            months = int(msd_proc[:-1])
            max_sentence = months / 12
            max_sentence_display = _pluralise('{} month{}', months)

        else:
            max_sentence = int(msd_proc)
            max_sentence_display = _pluralise('{} year{}', max_sentence)

        category_display = re.sub(r'^\d+[A-Z]? ', '', category.strip())

        yield {
            'title': code,
            'description': '{}\n\n{}\n\n{}'.format(
                offence.strip(),
                category_display,
                act,
            ),
            'order': max_sentence,
            'order_display': max_sentence_display,
        }
