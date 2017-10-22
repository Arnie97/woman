#!/usr/bin/env python3

import sys
import requests
import pyquery
import colorama

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
