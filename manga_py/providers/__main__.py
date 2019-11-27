from sys import stderr
from .meta import __version__

# File for cli info
# python -m manga_py.providers

print('Please, see https://github.com/manga-py/providers\nVersion: %s' % (__version__,), file=stderr)
