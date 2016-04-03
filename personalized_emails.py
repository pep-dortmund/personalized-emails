'''
A small python toolkit that creates and sends personalized
emails from `jinja2` templates and a pandas-readable database

Usage:
    personalized-emails <template> <database> [options]

Options:
    -c <config>, --config=<config>  config-file [default: config.cfg]
'''

import pandas as pd
import jinja2
import frontmatter
import gfm
import smtplib
from docopt import docopt
from configparser import RawConfigParser
from getpass import getpass


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


def setup_smtp_server(host, port, user, password=None):
    smtp = smtplib.SMTP_SSL(host, port)
    if password is None:
        password = getpass('Please enter your mail password: ')
    smtp.login(user, password)


def main():
    args = docopt(__doc__, version='PeP et Al. emails v0.0.1')
    database = read_database(args['<database>'])

    config = RawConfigParser()
    successful_files = config.read(args['--config'])
    if not successful_files:
        raise IOError('Could not read config-file')

    mail_server = setup_smtp_server(**config['smtp'])

    template, metadata = parse_template(args['<template>'])

    for recipient in database.itertuples():
        content = template.render(recipient=recipient)
        html = gfm.markdown(content)


if __name__ == '__main__':
    main()
