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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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

    return smtp


def build_mail(recipient, metadata, markdown, attachments=None):
    html = gfm.markdown(markdown)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = metadata['subject']
    msg['From'] = metadata.get('author', 'PeP et al. e.V.')
    msg['To'] = recipient.email

    plain_part = MIMEText(markdown, 'plain')
    html_part = MIMEText(html, 'html')

    msg.attach(plain_part)
    msg.attach(html_part)

    return msg


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

        markdown = template.render(recipient=recipient)

        attachments = metadata.get('attachments')
        mail = build_mail(recipient, metadata, markdown, attachments)

        mail_server.sendmail(
            metadata.get('author_email', 'kontakt@pep-dortmund.org'),
            recipient.email,
            mail.as_string(),
        )


if __name__ == '__main__':
    main()
