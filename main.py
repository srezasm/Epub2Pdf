#!/usr/bin/python

import ebooklib
from ebooklib import epub
import argparse
from os.path import splitext, isfile, dirname
from os import makedirs
from shutil import rmtree

parser = argparse.ArgumentParser(description='Convert EPUB to PDF')
parser.add_argument('-i', '--input', help='input epub file.', required=True)
parser.add_argument('-fs', '--font-size', type=int,
                    help='font size in pixels. default value: 15', default=15)
parser.add_argument('-o', '--output', help='output pdf file. default value: output.pdf',
                    default='./output.pdf')

TMP_DIR = 'epub2pdf-tmp'
def tmp_path(path): return f'{TMP_DIR}/{path}'


def main(args):
    # todo: find a better way to throw exception
    if not isfile(args.input):
        raise argparse.ArgumentError(None, "input file doesn't exist")
    if not splitext(args.input)[1] == '.epub':
        raise argparse.ArgumentError(None, 'input file is not en epub')

    book = epub.read_epub(args.input)
    items = book.get_items()
    for item in items:
        item_name = tmp_path(item.get_name())
        make_dirs(item_name)

        if item.get_type() == ebooklib.ITEM_STYLE:
            with open(item_name, 'w') as style_file:
                style_file.write(item.get_content().decode("utf-8"))

        elif item.get_type() == ebooklib.ITEM_COVER:
            with open(item_name, 'wb') as cover_file:
                cover_file.write(bytearray(item.get_content()))

        elif item.get_type() == ebooklib.ITEM_IMAGE:
            with open(item_name, 'wb') as image_file:
                image_file.write(bytearray(item.get_content()))

        elif item.get_type() == ebooklib.ITEM_FONT:
            with open(item_name, 'wb') as font_file:
                font_file.write(bytearray(item.get_content()))

        elif item.get_type() == ebooklib.ITEM_DOCUMENT:
            # todo: make html file with custom header
            with open(item_name, 'w') as doc_file:
                doc_file.write(item.get_content().decode("utf-8"))

        elif item.get_type() == ebooklib.ITEM_NAVIGATION:
            # todo: make html file with custom header
            with open(item_name, 'w') as nav_file:
                nav_file.write(item.get_content().decode("utf-8"))


def make_dirs(item_name):
    if dirname(item_name):
        makedirs(dirname(item_name), exist_ok=True)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
    rmtree(TMP_DIR)
