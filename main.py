#!/usr/bin/bash python

import argparse
import os
import pathlib
import sys
import tokenize

from parser import PythonParser


def get_args() -> None:
    """
    Gets command line arguments for the Python to parse
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', help='The full path of the Python file to be parsed into HTML')
    args = parser.parse_args()
    if not args.path:
        parser.error('\n[-] Expected a file to parse')
    if not os.path.isfile(args.path):
        parser.error('\n[-] File not found')
    if not os.path.isabs(args.path):
        parser.error('\n[-] Please provide the absolute path for the file')
    suffix = pathlib.Path(args.path).suffix
    if not suffix == '.py':
        parser.error(f'\n[-] Expected a Python (.py) file, not {suffix} file type')
    return args


def get_platform() -> None:
    """
    Returns the current platform for purposes of generating
    the correct path for the output file
    """
    return sys.platform


def write_html_file(html: str, platform: str) -> None:
    """
    Writes the html content generated from the PythonParser
    to a file and saves it in the current directory

    Args:
        html (str): the html to write to file
        platform (str): the platform the program is running on
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    if platform == "linux" or platform == "darwin":
        with open(f'{base_dir}/python_html.html', 'w+') as file:
            file.write(html)
    elif platform == "win32":
        with open(f'{base_dir}\python_html.html', 'w+') as file:
            file.write(html)


def main() -> None:
    """
    Main function for the Python_HTML_Parser app
    """
    args = get_args()
    platform = get_platform()
    print('\n[+] Writing HTML from Python source...')
    with open(args.path, 'r') as file:
        tokens = tokenize.generate_tokens(file.readline)
        python_parser = PythonParser(tokens)
        html = python_parser.generate_html()
        write_html_file(html, platform)
        print('[+] Writing complete!')
        if platform == "linux" or platform == "darwin":
            print(f'\n[+] You can find your file here: {args.path}/python_html.html\n')
        elif platform == "win32":
            print(f'\n[+] You can find your file here: {args.path}/python_html.html\n')


if __name__ == '__main__':
    main()

