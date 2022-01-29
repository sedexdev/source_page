#!/usr/bin/bash python

import argparse
import os
import pathlib
import platform
import sys
import themes
import tokenize

from source_parser import PythonParser
from typing import List


def theme_list() -> List:
    """
    Return a list of all available themes from
    themes.py

    Returns:
        A list of strings containing the names of all
        available themes
    """
    return ["cool_blue_light", "cyber", "robot", "robot_light"]


def get_theme(theme) -> str:
    """
    Get the theme from themes.py based on argument
    passed in by the user for --theme
    """
    theme_dict = {
        "cool_blue_light": themes.COOL_BLUE_LIGHT,
        "cyber": themes.CYBER,
        "robot": themes.ROBOT,
        "robot_light": themes.ROBOT_LIGHT
    }
    return theme_dict[theme]


def get_args() -> argparse.Namespace:
    """
    Gets command line arguments from the user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--path',
        dest='path',
        required=True,
        help='The full path of the Python file to be parsed into HTML')
    parser.add_argument('-t', '--theme', dest='theme', help='Syntax highlighting theme to use. Defaults to COOL_BLUE')
    parser.add_argument('-o', '--out', action='store_true', help='Send the output to stdout, not a file')
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
    theme = args.theme
    if theme and theme.lower() not in theme_list():
        parser.error("\n\n[-] Unknown theme: {}. See https://github.com/sedexdev/source_page for more\n".format(theme))
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
    path_dir = path_list[:len(path_list) - 1]
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
    base_dir = os.getcwd()
    if plat == "linux" or plat == "darwin":
        with open('{}/python_html.html'.format(base_dir), 'w') as file:
            file.write(html)
    elif plat == "win32":
        with open('{}\\python_html.html'.format(base_dir), 'w') as file:
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
    with open(args.path, 'r') as file:
        lines = file.readlines()
    with open(args.path, 'r') as file:
        tokens = tokenize.generate_tokens(file.readline)
        if args.theme:
            theme = get_theme(args.theme.lower())
            python_parser = PythonParser(tokens, is_updated, len(lines), theme)
        else:
            python_parser = PythonParser(tokens, is_updated, len(lines))
        html = python_parser.generate_html()
        if args.out:
            print(html)
        else:
            print('\n[+] Writing HTML from Python source...')
            if sys.platform == "linux" or sys.platform == "darwin":
                path = get_output_path("/", args)
            elif sys.platform == "win32":
                path = get_output_path("\\", args)
            write_html_file(html, sys.platform)
            print('[+] Writing complete!')
            print('\n[+] You can find your file here: {}python_html.html\n'.format(path))


if __name__ == '__main__':
    main()
