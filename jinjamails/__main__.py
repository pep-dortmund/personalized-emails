'''
A small python toolkit that creates and sends personalized
emails from `jinja2` templates and a pandas-readable database

Usage:
    personalized-emails <template> <database> [options]

Options:
    -c <config>, --config=<config>     config-file [default: config.cfg]
    -b <backend>, --backend=<backend>  mailing backend. If not given, the first backend
                                       description found in the configfile is used.
'''
from docopt import docopt
from configparser import RawConfigParser
import logging
import gfm

from . import read_database
from . import parse_template


def main():
    logging.basicConfig(level=logging.INFO)
    args = docopt(__doc__, version='PeP et Al. emails v0.0.1')
    database = read_database(args['<database>'])

    config = RawConfigParser()
    successful_files = config.read(args['--config'])
    if not successful_files:
        raise IOError('Could not read config-file')

    backend = args['--backend'] or config.sections()[0]

    if backend == 'smtplib':
        from .backends import SMTPLibMailer
        mailer = SMTPLibMailer(**config['smtplib'])

    elif backend == 'mailgun':
        from .backends import MailgunMailer
        mailer = MailgunMailer(**config['mailgun'])

    else:
        raise ValueError('Unsupported backend: {}'.format(args['--backend']))

    template, metadata = parse_template(args['<template>'])

    for recipient in database.itertuples():
        markdown = template.render(recipient=recipient, metadata=metadata)
        html = gfm.markdown(markdown)
        mailer.send_mail(
            recipient,
            metadata,
            markdown,
            html=html,
            attachments=metadata.get('attachments')
        )


if __name__ == '__main__':
    main()
