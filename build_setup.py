#!/urs/bin/env python3
# -*- coding: utf-8 -*-

from manga_py.providers import meta

with open('setup.py.template', 'r') as r:
    content = r.read()

    for key in meta.__all__:
        content = content.replace('__%s__' % key, getattr(meta, key))

    with open('setup.py', 'w') as w:
        w.write(content)

