from setuptools import setup


setup(
    name='jinjamail',
    version='0.1.0',
    description='Send personalized emails using jinja markdown templates',
    url='http://github.com/pep-dortmund/personalized-emails',
    author='Maximilian Noethe',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=[
        'jinjamails',
        'jinjamails.backends',
    ],
    entry_points={
        'console_scripts': ['jinjamails = jinjamails.__main__:main']
    },
    install_requires=[
        'pandas>=0.17.1',
        'gfm',
        'python-frontmatter',
        'jinja2',
        'docopt',
        'requests',
    ],
    zip_safe=False,
)
