import requests
import os
from . import Mailer


class MailgunMailer(Mailer):
    url_template = 'https://api.mailgun.net/v3/{domain}/messages'

    def __init__(self, domain, authkey):
        self.url = self.url_template.format(domain=domain)
        self.authkey = authkey

    def send_mail(self, recipient, metadata, plain_text, html=None, attachments=None):

        data = {
            'from': '{} <{}>'.format(
                metadata.get('author', 'PeP et. Al.'),
                metadata.get('author_email', 'kontakt@pep-dortmund.org'),
            ),

            'to': '{} {} <{}>'.format(
                recipient.firstname, recipient.lastname, recipient.email
            ),

            'subject': metadata['subject'],
            'text': plain_text
        }

        if html:
            data['html'] = html

        if attachments is not None:
            files = {}

            for i, attachment in enumerate(attachments):
                name = os.path.basename(attachment)

                files['attachment[{}]'.format(i)] = (name, open(attachment, 'rb'))

        else:
            files = None

        ret = requests.post(
            self.url,
            auth=("api", self.authkey),
            files=files,
            data=data,
        )
        ret.raise_for_status()
