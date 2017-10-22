#!/usr/bin/env python3

import sys
import pyquery
import colorama
from urllib.parse import urlencode

URL = 'https://explainshell.com/explain'


def main(argv):
    if not len(argv):
        print(__doc__)
        return
    params = urlencode({'cmd': ' '.join(argv)})
    full_url = URL + '?' + params
    parse(url=full_url)


def parse(*args, **kwargs):
    pq = pyquery.PyQuery(*args, **kwargs)
    results = pq('.help-box')
    if not results:
        print('manual missing')
    for result in results:
        text = []
        for element in pq(result).contents():
            if isinstance(element, str):
                text.append(element)
            else:
                text.append(colorama.Style.BRIGHT)
                text.append(element.text)
                text.append(colorama.Style.RESET_ALL)
        text.append('\n')
        print(''.join(text))


if __name__ == '__main__':
    main(sys.argv[1:])
