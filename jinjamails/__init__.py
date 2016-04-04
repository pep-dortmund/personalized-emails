import pandas as pd
import jinja2
import frontmatter


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
