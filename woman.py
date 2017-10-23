#!/usr/bin/env python3

'''woman - a command line interface for explainshell.com

Usage: woman <arguments> ...
Example: woman ls -lAdth
'''

import sys
import shutil
import pyquery
import colorama
from urllib.parse import urlencode

URL = 'https://explainshell.com/explain'


def main(argv=sys.argv[1:]):
    'Parse command line arguments.'
    colorama.init()
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
    print()
    lines = text.split('\n')
    indent = indent_test(lines[-1])

    # if the first line is not indented, do not append other lines to it
    if not indent_test(lines[0]):
        print(lines.pop(0))
        print(' ' * indent, end='')

    # otherwise, join all the lines to remove the line breaks
    if not lines:
        return
    text = ' '.join(line.strip() for line in lines)

    # split into lines again according to the terminal size
    while len(text) > columns:
        delimiter = len(text[:columns].rpartition(' ')[0])
        if not delimiter:
            break
        print(text[:delimiter])
        text = indent * ' ' + text[delimiter:].strip()
    print(text)


def indent_test(line):
    'Detect indentation of the given text.'
    line = strip_ansi(line)

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


def strip_ansi(text):
    'Remove ANSI escape codes from the text.'
    escape_codes = [
        colorama.Style.BRIGHT,
        colorama.Style.RESET_ALL,
    ]
    for escape_code in escape_codes:
        text = text.replace(escape_code, '')
    return text


if __name__ == '__main__':
    main()
