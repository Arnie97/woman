#!/usr/bin/env python3

import sys
import shutil
import pyquery
import colorama
from urllib.parse import urlencode

URL = 'https://explainshell.com/explain'


def main(argv):
    'Parse command line arguments.'
    if not len(argv):
        print(__doc__)
        return
    params = urlencode({'cmd': ' '.join(argv)})
    full_url = URL + '?' + params
    columns = shutil.get_terminal_size().columns
    for section in parse(url=full_url):
        reflow(section, columns)


def parse(*args, **kwargs):
    'Extract manual pages from the HTML document.'
    pq = pyquery.PyQuery(*args, **kwargs)
    results = pq('.help-box')
    if not results:
        yield 'manual missing'
    for result in results:
        text = []
        for element in pq(result).contents():
            if isinstance(element, str):
                text.append(element)
            else:
                text.append(colorama.Style.BRIGHT)
                text.append(element.text)
                text.append(colorama.Style.RESET_ALL)
        yield ''.join(text)


def reflow(text, columns):
    'Fit display to terminal size.'
    lines = text.split('\n')
    indent = indent_test(lines[-1])
    text = ' '.join(line.strip() for line in lines)

    while len(text) > columns:
        delimiter = len(text[:columns].rpartition(' ')[0])
        if not delimiter:
            break
        print(text[:delimiter])
        text = indent * ' ' + text[delimiter:].strip()
    print(text, end='\n\n')


def indent_test(line):
    'Detect indentation of the given text.'
    # skip optional non-whitespace characters
    for i, char in enumerate(line):
        if char.isspace():
            break
    else:  # reached the end of line
        return 0

    # count space characters
    for j, char in enumerate(line[i:]):
        if not char.isspace():
            return i + j if j > 1 else 0  # more than one space
    else:  # reached the end of line
        return 0


if __name__ == '__main__':
    main(sys.argv[1:])
