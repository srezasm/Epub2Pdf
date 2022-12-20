#!/usr/bin/python

import ebooklib
from ebooklib import epub
import argparse
from os.path import splitext, isfile

parser = argparse.ArgumentParser(description='Convert EPUB to PDF')
parser.add_argument('-i', '--input', help='input epub file.', required=True)
parser.add_argument('-fs', '--font-size', type=int,
                    help='font size in pixels. default value: 15', default=15)
parser.add_argument('-o', '--output', help='output pdf file. default value: output.pdf',
                    default='./output.pdf')


args = parser.parse_args()


def main():
    #todo: find a better way to throw exception
    if not isfile(args.input):
        raise argparse.ArgumentError(None, "input file doesn't exist")
    if not splitext(args.input) == 'epub':
        raise argparse.ArgumentError(None, 'input file is not epub')

    book = epub.read_epub(args.input)
    book.get_items()

    print(args.output)


if __name__ == '__main__':
    main()
