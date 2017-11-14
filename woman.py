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
    'Fit the text block into the terminal.'
    print()
    lines = text.split('\n')
    indent = indent_test(lines[-1])
    spaces = header_test(lines, indent)

    # join all the remaining lines to remove the line breaks
    text = ' '.join(line.strip() for line in lines)
    plain_text = strip_ansi(text)

    # split into words again
    words = text.split()
    plain_words = plain_text.split()

    # fit into lines according to the terminal size
    while len(' '.join(plain_words)) > columns - indent:
        line_length = indent
        for i in range(len(plain_words)):
            line_length += len(plain_words[i]) + 1
            if line_length > columns:
                print(' ' * spaces + ' '.join(words[:i]))
                if spaces != indent:
                    spaces = indent
                words = words[i:]
                plain_words = plain_words[i:]
                break

    # print the last line
    print(' ' * spaces + ' '.join(words))


def header_test(lines, indent):
    'Print the header line with proper spaces.'
    # if the first line contains no options, just reflow it
    if not strip_ansi(lines[0]).startswith('-'):
        return indent

    # if the first line contains both options and explanations
    # keep the option part untouched, but reflow the explanation part
    elif indent_test(lines[0]) == indent:
        # count words in the option part, i.e. before the indent
        words_in_options = strip_ansi(lines[0])[:indent].split()
        n = len(words_in_options)

        # print the corresponding colored text for that part
        words = lines[0].split()
        print(' '.join(words[:n]), end='')
        lines[0] = ' '.join(words[n:])

        # reduce spaces
        return indent - len(' '.join(words_in_options))

    # if the first line contains only options, do not reflow it
    else:
        print(lines.pop(0))
        return indent


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
