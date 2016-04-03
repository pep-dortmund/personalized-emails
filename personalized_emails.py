'''
A small python toolkit that creates and sends personalized
emails from `jinja2` templates and a pandas-readable database

Usage:
    personalized-emails <template> <database> [options]

Options:
    -c <config>, --config=<config>  config-file [default: config.cfg]
'''

import os
import pandas as pd
import jinja2
import frontmatter
import gfm
import smtplib
import mimetypes
from docopt import docopt
from configparser import RawConfigParser
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders


def read_database(inputfile, **kwargs):
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

    mail = MIMEMultipart()
    mail['Subject'] = metadata['subject']
    mail['From'] = '{} <{}>'.format(
        metadata.get('author', 'PeP et al. e.V.'),
        metadata.get('author_email', 'kontakt@pep-dortmund.org'),
    )
    mail['To'] = recipient.email

    msg = MIMEMultipart('alternative')
    plain_part = MIMEText(markdown, 'plain')
    html_part = MIMEText(html, 'html')

    msg.attach(plain_part)
    msg.attach(html_part)

    mail.attach(msg)

    if attachments is not None:
        for attachment in attachments:
            filename = os.path.basename(attachment)
            ctype, encoding = mimetypes.guess_type(attachment)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'

            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(attachment) as fp:
                    # Note: we should handle calculating the charset
                    att = MIMEText(fp.read(), _subtype=subtype)
            elif maintype == 'image':
                with open(attachment, 'rb') as fp:
                    att = MIMEImage(fp.read(), _subtype=subtype)
            else:
                with open(attachment, 'rb') as fp:
                    att = MIMEBase(maintype, subtype)
                    att.set_payload(fp.read())
                # Encode the payload using Base64
                encoders.encode_base64(att)
            # Set the filename parameter
            att.add_header('Content-Disposition', 'attachment', filename=filename)
            mail.attach(att)

    return mail


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
            '{} <{}>'.format(
                metadata.get('author', 'PeP et al. e.V.'),
                metadata.get('author_email', 'kontakt@pep-dortmund.org'),
            ),
            recipient.email,
            mail.as_string(),
        )


if __name__ == '__main__':
    main()
