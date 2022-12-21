#!/usr/bin/python

import ebooklib
from ebooklib import epub
import argparse
from os.path import splitext, isfile, dirname
from pathlib import Path
from os import makedirs, getcwd
from shutil import rmtree

parser = argparse.ArgumentParser(description='Convert EPUB to PDF')
parser.add_argument('-i', '--input', help='input epub file.', required=True)
parser.add_argument('-fs', '--font-size', type=int,
                    help='font size in pixels. default value: 15', default=15)
parser.add_argument('-o', '--output', help='output pdf file. default value: output.pdf',
                    default='./output.pdf')

TMP_DIR = 'epub2pdf-tmp'
CWD = getcwd()
def tmp_path(path): return f'{CWD}/{TMP_DIR}/{path}'


document_html = '<!DOCTYPE html><html><head>{header}</head><body>{{body}}</body></html>'
stylesheet_tag = '<link rel="stylesheet" href="{href}">'


def main(args):
    # todo: find a better way to throw exception
    if not isfile(args.input):
        raise argparse.ArgumentError(None, "input file doesn't exist")
    if not splitext(args.input)[1] == '.epub':
        raise argparse.ArgumentError(None, 'input file is not en epub')

    docs = []
    styles = []
    book = epub.read_epub(args.input)
    items = book.get_items()

    for item in items:
        item_name = tmp_path(item.get_name())
        make_dirs(item_name)

        # styles
        if item.get_type() == ebooklib.ITEM_STYLE:
            styles.append(stylesheet_tag.format(
                href=tmp_path(item.get_name())))
            with open(item_name, 'w') as style_file:
                style_file.write(item.get_content().decode("utf-8"))

        # cover
        elif item.get_type() == ebooklib.ITEM_COVER:
            with open(item_name, 'wb') as cover_file:
                cover_file.write(bytearray(item.get_content()))

        # images
        elif item.get_type() == ebooklib.ITEM_IMAGE:
            with open(item_name, 'wb') as image_file:
                image_file.write(bytearray(item.get_content()))

        # fonts
        elif item.get_type() == ebooklib.ITEM_FONT:
            with open(item_name, 'wb') as font_file:
                font_file.write(bytearray(item.get_content()))

    # documents
    imported_styles_html = ''.join(styles)
    formatted_document_html = document_html.format(header=imported_styles_html)
    items = book.get_items()
    for doc in items:
        if doc.get_type() != ebooklib.ITEM_DOCUMENT:
            continue

        doc_name = tmp_path(doc.get_name())
        doc_name = str(Path(doc_name).with_suffix('.html'))
        make_dirs(doc_name)

        docs.append(doc_name)
        with open(doc_name, 'w') as doc_file:
            doc_file.write(
                formatted_document_html.format(
                    body=doc.get_body_content().decode("utf-8")
                )
            )


def make_dirs(item_name):
    if dirname(item_name):
        makedirs(dirname(item_name), exist_ok=True)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
    rmtree(TMP_DIR)
