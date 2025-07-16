"""
Python parser module
"""

from themes import COOL_BLUE
from tokenize import TokenInfo
from typing import Iterator, Tuple

from vars import (
    keywords,
    special_keywords,
    token_map
)


def has_str_prefix(value: str) -> bool:
    """
    Inspect a token value of type string to check if it has a
    prefix or contains escaped characters.

    Args:
        value (str): the string value of this token
    Returns:
        Boolean defining whether value has a prefix
    """
    string_prefix = ["r", "u", "R", "U", "f", "F", "fr", "Fr", "fR", "FR", "rf", "rF", "Rf", "RF"]
    bytes_prefix = ["b", "B", "br", "Br", "bR", "BR", "rb", "rB", "Rb", "RB"]
    return value[0] in string_prefix or value[0] in bytes_prefix


def is_multi_line(value: str) -> bool:
    """
    Checks the starting character of the token value passed in
    to see if it is a multi line string

    Args:
        value (str): string value of this token
    Returns:
        Boolean stating whether this is a multi line string
    """
    return value.startswith("\"\"\"") or value.startswith("'''")


def get_span_class(token: TokenInfo) -> Tuple:
    """
    Allocates the correct CSS class to an HTML span element
    representing the current token

    Args:
        token (TokenInfo): the token to inspect
    """
    token_type = token_map[token.type]
    token_value = token.string
    if token_type == "OP":
        return "python-op", None
    if token_type == "COMMENT":
        return "python-comment", None
    if token_type == "STRING":
        prefixed = has_str_prefix(token_value)
        return "python-str", prefixed
    if token_value in keywords:
        return "python-keyword", None
    if token_value in special_keywords:
        return "python-special-keyword", None
    return "python-txt", None


class PythonParser:
    """
    Defines functions for parsing tokenized Python
    source code and building a syntax highlighted HTML page
    from the result
    """

    def __init__(self, tokens: Iterator, file_length: int, theme=COOL_BLUE) -> None:
        """
        Constructor for the PythonParser class

        Args:
            tokens (SupportsNext): a list of tokens
            is_updated (bool): states if Python version is using
                               an updated token ID dictionary
            file_length (int): number of lines in the file
            theme (str): colour scheme for syntax highlighting
        """
        self.tokens = tokens
        self.file_length = file_length
        self.theme = theme
        self.html = ""
        self.line_number = 1

    def add_line_helper(self, max_lines: int) -> None:
        """
        Adds the line number in a span element

        Args:
            max_lines (int): maximum number of lines
        """
        max_lines_len = len(str(max_lines))
        line_num_len = len(str(self.line_number))
        spacer = "&nbsp;" * (max_lines_len - line_num_len)
        self.html += f"<span class='line-number'>{spacer}{self.line_number}.&nbsp;</span>"

    def add_line_number(self) -> None:
        """
        Assesses the file length and calls the helper
        function with the appropriate parameters for
        a file with self.file_length many lines
        """
        if self.file_length < 10:
            self.add_line_helper(9)
        elif self.file_length < 100:
            self.add_line_helper(99)
        elif self.file_length < 1000:
            self.add_line_helper(999)
        elif self.file_length < 10000:
            self.add_line_helper(9999)
        else:
            self.add_line_helper(99999)

    def delete_line(self) -> None:
        """
        Delete the last code line added to the self.html string in
        the case that a multi-line string has been found. This
        stops nested code lines and allows the multi-line
        string to be added on separate lines, as it appears
        in the Python source code
        """
        last_code_line = self.html.rfind("<c")
        self.html = self.html[:last_code_line]

    def handle_multi_line_str(self, value: str, spacer: str, inline=False) -> None:
        """
        Create a series of code blocks representing a multi-line
        string in the source code with preserved indentation

        Args:
            value (str): The string value to process
            spacer (str): amount of whitespace to add
            inline (bool): states that this string is inline with
                           other code on the same line
        """
        first = True
        string_split = value.split("\n")
        for s in string_split:
            if first and not inline:
                total_spacer = spacer
                first = False
            else:
                whitespace = len(s) - (len(s.lstrip(" ")))
                total_spacer = "&nbsp;" * (whitespace - 1)
            self.html += "<code class=\"code-line\">"
            self.add_line_number()
            self.html += f"<span class=\"python-str\">{total_spacer}{s}</span>"
            self.html += "</code>"
            self.line_number += 1

    def handle_string(self, value: str, prev_value: str, prefixed: bool, spacer: str) -> bool:
        """
        Adds a string token to the HTML file by checking to
        see if the string has a prefix, is a multi-line string,
        or is just a regular string

        Args:
            value (str): token string value
            prev_value (str): value of the previous token
            prefixed (bool): states whether the string is prefixed
            spacer (str): amount of whitespace to add
        """
        if prefixed:
            self.html += f"<span class=\"python-str-prefix\">{spacer}{value[0]}</span>"
            value = value[1:]
        if is_multi_line(value):
            if prev_value == "=":
                first_str = value.split("\n")[0]
                self.html += f"<span class=\"python-str\">{spacer}{first_str}</span>"
                self.html += "</code>\n"
                self.line_number += 1
                self.handle_multi_line_str(value[len(first_str) + 1:], spacer, True)
                return True
            self.delete_line()
            self.handle_multi_line_str(value, spacer)
            return True
        else:
            if prefixed:
                self.html += f"<span class=\"python-str\">{value}</span>"
            else:
                self.html += f"<span class=\"python-str\">{spacer}{value}</span>"
            return False

    def handle_comment(self, start: int, value: str) -> None:
        """
        Create a code block and span element to represent a
        comment from the Python source code

        Args:
            start (int): starting column of comment
            value (str): string value of the token
        """
        self.html += "<code class=\"code-line\">"
        self.add_line_number()
        spacer = "&nbsp;" * start
        self.html += f"<span class=\"python-comment\">{spacer}{value}</span>"
        self.html += "</code>"
        self.line_number += 1

    def handle_nl(self) -> None:
        """
        Create an empty code block with a line number when a blank
        line needs to be inserted
        """
        self.html += "<code class=\"code-line\">"
        self.add_line_number()
        self.html += "</code>"
        self.line_number += 1

    def parse(self) -> None:
        """
        Parses the Python source code one token at a time, creating
        HTML elements of each line and writing the result to the
        output file.
        """
        prev_token_was_multi_line = False

        while True:

            token = next(self.tokens, None)

            if not token or token.type == "ENDMARKER":
                break

            token_type = token_map[token.type]

            token_value = token.string
            prev_token_value = ""
            prev_token_start = 0
            prev_token_length = 0
            parse_broken = False
            token_start = token.start[1]

            if prev_token_was_multi_line:
                prev_token_was_multi_line = False
                continue

            if token_type == "COMMENT":
                print("FOUND COMMENT")
                self.handle_comment(token_start, token_value)
                next(self.tokens, None)
                continue

            if token_type == "NL":
                self.handle_nl()
                continue

            if token_type == "INDENT" or token_type == "DEDENT":
                continue

            self.html += "<code class=\"code-line\">"
            self.add_line_number()
            first = True

            line_join = False

            while token_type != "NEWLINE":

                if line_join:
                    self.html += "<code class=\"code-line\">"
                    self.add_line_number()
                    first = True

                if token_type == "NL":
                    break

                if first:
                    spacer = "&nbsp;" * token_start
                    first = False
                else:
                    spacer = "&nbsp;" * (token_start - (prev_token_start + prev_token_length))

                span_class, prefixed = get_span_class(token)

                if token_type == "STRING":
                    break_parse = self.handle_string(token_value, prev_token_value, prefixed, spacer)
                    if break_parse:
                        parse_broken = True
                        prev_token_was_multi_line = True
                        break
                elif not prefixed:
                    self.html += f"<span class=\"{span_class}\">{spacer}{token_value}</span>"

                prev_token_value = token_value
                prev_token_start = token_start
                prev_token_end = token.end[1]
                prev_token_length = len(str(token_value))

                token = next(self.tokens, None)

                if not token or token_type == "ENDMARKER":
                    break

                token_type = token_map[token.type]

                token_value = token.string
                token_start = token.start[1]

                if token_start < prev_token_end:
                    self.html += "<span class='python-op'>&nbsp;\\</span>"
                    self.html += "</code>"
                    self.line_number += 1
                    line_join = True
                else:
                    line_join = False

            if not parse_broken:
                self.html += "</code>"
                self.line_number += 1

    def add_html_meta(self) -> None:
        """
        Adds the metadata to the HTML string
        """
        self.html += ("<!DOCTYPE html>\n"
                      "<html lang='en'>\n"
                      "    <head>\n"
                      "    <meta charset='UTF-8'>\n"
                      "    <meta http-equiv='X-UA-Compatible' content='IE=edge'>\n"
                      "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
                      "    <title>SourcePage Output HTML</title>\n"
                      "    <style>\n"
                      f"{self.theme}\n"
                      "    </style>\n"
                      "    </head>\n"
                      "    <body>\n"
                      "        <div class='code-block python-code-block'>\n"
                      )

    def close_html(self) -> None:
        """
        Adds the closing tags to the HTML string
        """
        self.html += ("        </div>\n"
                      "    </body>\n"
                      "</html>")

    def generate_html(self) -> str:
        """
        Generates the HTML representation of the Python
        source code

        Returns:
            Value of self.html
        """
        self.add_html_meta()
        self.parse()
        self.close_html()
        return self.html
