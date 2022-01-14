#!/usr/bin/bash python

import argparse
import os
import pathlib
import platform
import sys
import tokenize

from parser import PythonParser


def get_args() -> argparse.Namespace:
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


def python_updated():
    """
    Checks the version of Python that was used to run the
    program so the correct list of token IDs can be
    referrenced during parsing

    Returns:
        Boolean stating whether the program should use
        the updated token ID dictionary
    """
    version = platform.python_version_tuple()
    if int(version[0]) >= 3 and int(version[1]) >= 10:
        return True
    return False


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
    is_updated = python_updated()
    print('\n[+] Writing HTML from Python source...')
    with open(args.path, 'r') as file:
        tokens = tokenize.generate_tokens(file.readline)
        python_parser = PythonParser(tokens, is_updated)
        html = python_parser.generate_html()
        write_html_file(html, sys.platform)
        print('[+] Writing complete!')
        if sys.platform == "linux" or sys.platform == "darwin":
            print(f'\n[+] You can find your file here: {args.path}/python_html.html\n')
        elif sys.platform == "win32":
            print(f'\n[+] You can find your file here: {args.path}\python_html.html\n')


if __name__ == '__main__':
    main()

