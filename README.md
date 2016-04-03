# personalized-emails


This is a small tool to send personalized emails based on a `recipients.json`
file and a markdown template, providing some metadata in a `yaml` header.


## recipients.json

This file contains the recipients of the mails like this:
```json
[
	{"firstname": "John", "lastname": "Doe", "email": "john.doe@tu-dortmund.de"},
	{"firstname": "Jane", "lastname": "Doe", "email": "jane.doe@tu-dortmund.de"}
]
```

If you can add more fields, if you want.


## Writing a template

This tool uses `markdown` with the `jinja2` templating language.
One record in the `json` file is passed to the template as `recipient`.

To access an element, you can use:
```
{{ recipient.firstname }}
```

### metadate: subject, author, ...
Metadata is given in a `yaml` header on top of the template:

```
---
subject: My first try with personalized email
author: me
author_email: me@example.com
---
```

### Add attachments

Use the `attachments` meta tag to add attachments:

```
---
subject: My first try with personalized email
author: me
author_email: me@example.com
attachments: 
    - /path/to/attachment
---
```


## Mail server configuration

The tool will look for a config.cfg in the current directory containing
the mail server configuration like this:
```
[smtp]
host: ...
port: ...
user: ...
```

You can also provide a `password`, if not, you will be asked for it.
You set the path of the configfile using the `-c /path/to/config/file` option.

## Running the program

To send the mails, do
```
python personalized_emails.py /path/to/template.md /path/to/recipients.json
```
