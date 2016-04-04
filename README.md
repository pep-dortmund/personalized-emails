# jinjamails

This is a small tool to send personalized emails based on a `recipients.json`
file and a markdown template, providing some metadata in a `yaml` header.

## Install

Use 
```
pip install https://github.com/pep-dortmund/personalized-emails/archive/v0.1.0.tar.gz
```

## Running the program

To send the mails, do
```
jinjamails /path/to/template.md /path/to/recipients.json [options]
```


## Recipients

Recipients are currently read from a `json` file like this:
```json
[
  {"firstname": "John", "lastname": "Doe", "email": "john.doe@tu-dortmund.de"},
  {"firstname": "Jane", "lastname": "Doe", "email": "jane.doe@tu-dortmund.de"}
]
```
These are the required fields to send an email. 
You can add more, which you can then use in the templates.

We plan to support more database / file types.


## Writing a template

This tool uses `markdown` with the `jinja2` templating language.
One record of the recipient database is passed to the template as `recipient`.

To access an element, you can use:
```
{{ recipient.firstname }}
```

For more possibilities, have a look into the `jinja2` [docs](http://jinja.pocoo.org/).


### metadate: subject, author, ...
Metadata is given in a `yaml` header on top of the template:

```
---
subject: My first try with personalized email
author: me
author_email: me@example.com
---
```

You also have access to the metadate in the templates, e.g. using
```
Cheers
{{ metadata.author }}
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

We currently support two backends:
* smtp via the python standard library modules `smtplib` and `email`
* mailgun via `requests`

`smtp` is the default.

The tool will look for a config.cfg or
you set the path of the configfile using the `-c /path/to/config/file` option.

### smtp

```
[smtplib]
host: ...
port: ...
user: ...
```

You can also provide a `password`, if not, you will be asked for it.

### Mailgun

If you want to use Mailgun, put this into your config file:
```
[mailgun]
domain: ...
authkey: ...
```
And start `jinjamail` with `-b mailgun`

