from sys import stderr
from .meta import version

# File for cli info
# python -m manga_py.providers

print('Please, see https://github.com/manga-py/providers\nVersion: %s' % (version,), file=stderr)
