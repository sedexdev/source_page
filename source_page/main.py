#!/usr/bin/bash python

import argparse
import os
import pathlib
import platform
import sys
import themes
import tokenize

from source_parser import PythonParser
from vars import theme_list


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
    parser.add_argument('-o', '--output', action='store_true', help='Send the output to a file')
    args = parser.parse_args()
    if not args.path:
        parser.error('\n\n[-] Expected a file to parse\n')
    if not os.path.isfile(args.path):
        parser.error('\n\n[-] File not found\n')
    suffix = pathlib.Path(args.path).suffix
    if not suffix == '.py':
        parser.error('\n\n[-] Expected a Python (.py) file, not {} file type\n'.format(suffix))
    theme = args.theme
    if theme and theme.lower() not in theme_list:
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
    return int(version[0]) >= major and int(version[1]) >= minor


def get_source_path(path: str) -> str:
    """
    Get the path to the file that is going to be read

    Args:
        path (str): the file path provided by the user
    """
    if os.path.isabs(path):
        return path
    return os.path.join(os.getcwd(), path)


def pretty_html(html: str) -> str:
    """
    Add padding at the beginning of code and span
    elements to format the HTML output

    Args:
        html (str): the HTML output string
    """
    format_html = html
    format_html = format_html.replace("<code", "\n{}<code".format(" " * 12))
    format_html = format_html.replace("<span", "\n{}<span".format(" " * 16))
    format_html = format_html.replace("</code>", "\n{}</code>\n".format(" " * 12))
    return format_html


def write_html_file(html: str, plat: str) -> None:
    """
    Writes the html content generated from the PythonParser
    to a file and saves it in the current directory

    Args:
        html (str): the html to write to file
        plat (str): the platform the program is running on
    """
    print('\n[+] Writing HTML from Python source...')
    base_dir = os.getcwd()
    if plat == "win32":
        with open('{}\\output.html'.format(base_dir), 'w') as file:
            file.write(html)
            print('[+] Writing complete!')
            print('\n[+] You can find your file here: {}\\output.html\n'.format(os.getcwd()))
    else:
        with open('{}/output.html'.format(base_dir), 'w') as file:
            file.write(html)
            print('[+] Writing complete!')
            print('\n[+] You can find your file here: {}/output.html\n'.format(os.getcwd()))


def main() -> None:
    """
    Main function for the SourcePage tool. Gets
    arguments from the command line to build and
    write a HTML string that can be sent to stdout
    or written directly to a .html file
    """
    if not check_py_version(3, 6):
        print("\n[-] This program requires Python3.6 or later!")
        print("[-] Please upgrade now!\n")
        return
    args = get_args()
    is_updated = check_py_version(3, 10)
    full_path = get_source_path(args.path)
    try:
        with open(full_path, 'r') as file:
            lines = file.readlines()
        with open(full_path, 'r') as file:
            tokens = tokenize.generate_tokens(file.readline)
            if args.theme:
                theme = get_theme(args.theme.lower())
                python_parser = PythonParser(tokens, is_updated, len(lines), theme)
            else:
                python_parser = PythonParser(tokens, is_updated, len(lines))
            html = python_parser.generate_html()
            if not args.output:
                print(pretty_html(html))
            else:
                write_html_file(html, sys.platform)
    except FileNotFoundError:
        print("\n[-] File not found")


if __name__ == '__main__':
    main()
