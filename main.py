#!/usr/bin/bash python

import argparse
import os
import pathlib
import platform
import sys
import tokenize

from pytml_parser import PythonParser


def get_args() -> argparse.Namespace:
    """
    Gets command line arguments from the user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', help='The full path of the Python file to be parsed into HTML')
    args = parser.parse_args()
    if not args.path:
        parser.error('\n\n[-] Expected a file to parse\n')
    if not os.path.isfile(args.path):
        parser.error('\n\n[-] File not found\n')
    if not os.path.isabs(args.path):
        parser.error('\n\n[-] Please provide the absolute path for the file\n')
    suffix = pathlib.Path(args.path).suffix
    if not suffix == '.py':
        parser.error('\n\n[-] Expected a Python (.py) file, not {} file type\n'.format(suffix))
    return args


def check_py_version(major: int, minor: int) -> bool:
    """
    Checks the version of Python that was used to run the
    program to see if it is greater than or equal to the
    values passed in

    Args:
        major (int): the major release version
        minor (int): the minor release version

    Returns:
        Boolean stating whether the Python version meets
        the values in the parameters
    """
    version = platform.python_version_tuple()
    if int(version[0]) >= major and int(version[1]) >= minor:
        return True
    return False


def get_output_path(delimiter: str, args: argparse.Namespace) -> str:
    """
    Creates a string representation of the absolute path
    for the parent directory of the HTML output file

    Args:
        delimiter (str): the path delimiter
        args (Namespace): command line arguments

    Returns:
        A string of the parent directory for the HTML file
    """
    path_list = args.path.split(delimiter)
    path_dir = path_list[:len(path_list)-1]
    path = delimiter.join([x for x in path_dir])
    return "{x}{y}".format(x=path, y=delimiter)


def write_html_file(html: str, plat: str) -> None:
    """
    Writes the html content generated from the PythonParser
    to a file and saves it in the current directory

    Args:
        html (str): the html to write to file
        plat (str): the platform the program is running on
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    if plat == "linux" or plat == "darwin":
        with open('{}/python_html.html'.format(base_dir), 'w+') as file:
            file.write(html)
    elif plat == "win32":
        with open('{}\\python_html.html'.format(base_dir), 'w+') as file:
            file.write(html)


def main() -> None:
    """
    Main function for the Python_HTML_Parser app
    """
    if not check_py_version(3, 6):
        print("\n[-] This program requires Python3.6 or later!")
        print("[-] Please upgrade now!\n")
        return
    args = get_args()
    is_updated = check_py_version(3, 10)
    print('\n[+] Writing HTML from Python source...')
    with open(args.path, 'r') as file:
        lines = file.readlines()
    with open(args.path, 'r') as file:
        tokens = tokenize.generate_tokens(file.readline)
        python_parser = PythonParser(tokens, is_updated, len(lines))
        html = python_parser.generate_html()
        write_html_file(html, sys.platform)
        print('[+] Writing complete!')
        if sys.platform == "linux" or sys.platform == "darwin":
            path = get_output_path("/", args)
        elif sys.platform == "win32":
            path = get_output_path("\\", args)
        print('\n[+] You can find your file here: {}python_html.html\n'.format(path))


if __name__ == '__main__':
    main()
