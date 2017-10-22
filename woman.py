#!/usr/bin/env python3

import sys
import requests
import pyquery

URL = 'https://explainshell.com/explain'


def main(argv):
    if not len(argv):
        print(__doc__)
        return
    response = requests.get(URL, {'cmd': ' '.join(argv)})
    parse(response.text)


def parse(page):
    pq = pyquery.PyQuery(page)
    results = pq('.help-box')
    if not results:
        print('manual missing')
    for result in results:
        print(result.text_content())


if __name__ == '__main__':
    main(sys.argv[1:])
