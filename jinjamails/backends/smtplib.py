import smtplib
import os
import mimetypes
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

from . import Mailer


class SMTPLibMailer(Mailer):
    def __init__(self, host, port, user, password=None):
        self.server = smtplib.SMTP_SSL(host, port)
        if password is None:
            password = getpass('Please enter your mail password: ')

        self.server.login(user, password)

    def send_mail(self, recipient, metadata, plain_text, html=None, attachments=None):

        mail = MIMEMultipart()
        mail['Subject'] = metadata['subject']
        mail['From'] = '{} <{}>'.format(
            metadata.get('author', 'PeP et al. e.V.'),
            metadata.get('author_email', 'kontakt@pep-dortmund.org'),
        )
        mail['To'] = recipient.email

        if html:
            msg = MIMEMultipart('alternative')
            plain_part = MIMEText(plain_text, 'plain')
            html_part = MIMEText(html, 'html')

            msg.attach(plain_part)
            msg.attach(html_part)
        else:
            msg = MIMEText(plain_text, 'plain')

        mail.attach(msg)

        if attachments is not None:
            for attachment in attachments:
                filename = os.path.basename(attachment)
                ctype, encoding = mimetypes.guess_type(attachment)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'

                maintype, subtype = ctype.split('/', 1)

                if maintype == 'text':
                    with open(attachment) as fp:
                        att = MIMEText(fp.read(), _subtype=subtype)

                elif maintype == 'image':
                    with open(attachment, 'rb') as fp:
                        att = MIMEImage(fp.read(), _subtype=subtype)

                else:
                    with open(attachment, 'rb') as fp:
                        att = MIMEBase(maintype, subtype)
                        att.set_payload(fp.read())
                    encoders.encode_base64(att)

                att.add_header('Content-Disposition', 'attachment', filename=filename)
                mail.attach(att)

        self.server.sendmail(
            from_addr='{} <{}>'.format(
                metadata.get('author', 'PeP et al. e.V.'),
                metadata.get('author_email', 'kontakt@pep-dortmund.org'),
            ),
            to_addrs=recipient.email,
            msg=mail.as_string(),
        )
