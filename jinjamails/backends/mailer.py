class Mailer:
    def send_mail(self, recipient, metadata, plain_text, html=None, attachments=None):
        raise NotImplementedError
