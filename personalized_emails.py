'''
A small python toolkit that creates and sends personalized
emails from `jinja2` templates and a pandas-readable database

Usage:
    personalized-emails <template> <database>
'''
import jinja2
import pandas as pd
from tqdm import tqdm
from docopt import docopt
import frontmatter
import gfm


def read_database(inputfile, **kwargs):

    if inputfile.endswith('.csv'):
        database = pd.read_csv(
            inputfile,
            delimiter='|',
            dtype={'Kontonummer': str, 'BLZ': str, 'Abschlussjahrgang': str},
        )
        return database

    if inputfile.endswith('.json'):
        database = pd.read_json(
            inputfile,
            orient='records',
        )
        return database

    raise IOError('Not supported database format')


def parse_template(inputfile):
    result = frontmatter.load(inputfile)
    template = jinja2.Template(result.content)

    return template, result.metadata


def main():
    args = docopt(__doc__, version='PeP et Al. emails v0.0.1')
    database = read_database(args['<database>'])

    template, metadata = parse_template(args['<template>'])

    for recipient in database.itertuples():
        content = template.render(recipient=recipient)
        html = gfm.markdown(content)

        with open('test_{}.html'.format(recipient.firstname), 'w') as f:
            f.write(html)


if __name__ == '__main__':
    main()

