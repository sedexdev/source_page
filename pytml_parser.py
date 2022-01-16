from tokenize import TokenInfo
from typing import Iterable, Tuple

from vars import (
    keywords,
    special_keywords,
    token_ids,
    token_ids_new
)


class PythonParser():

    """
    Defines functions for parsing tokenized Python
    source code and building a syntax highlighted HTML page
    from the result
    """

    CSS = """
    .code {
        font-weight: bold;
    }
    .code-block {
        display: flex;
        flex-direction: column;
        background-color: lightgrey;
        border: 1px dashed #333;
        text-align: left;
        font-size: 1.1rem;
        overflow-x: scroll;
        white-space: nowrap;
        padding: 20px;
    }
    .code-line {
        margin: 3px 0;
    }
    .python-code-block {
        background-color: #333;
        margin: 40px 0;
    }
    .python-class,
    .python-var,
    .python-func,
    .python-op,
    .python-str,
    .python-str-prefix,
    .python-keyword,
    .python-special-keyword,
    .python-comment,
    .line-number {
        font-size: 1.1rem;
    }
    .python-var {
        color: skyblue;
    }
    .python-op {
        color: #fff;
    }
    .python-str {
        color: tomato;
    }
    .python-str-prefix {
        color: orange;
    }
    .python-keyword {
        color: rgb(87, 62, 245);
    }
    .python-special-keyword {
        color: rgb(159, 66, 253);
    }
    .python-comment {
        color: rgb(25, 129, 25);
    }
    .line-number {
        color: #666;
    }
    """

    def __init__(self, tokens: Iterable, is_updated: bool, file_length: int) -> None:
        """
        Constructor for the PythonParser class

        Args:
            tokens (Iterable): a list of tokens
            is_updated (bool): states if Python version is using
                               an updated token ID dictionary
            file_length (int): number of lines in the file
        """
        self.tokens = tokens
        self.is_updated = is_updated
        self.file_length = file_length
        self.html = ""
        self.line_number = 1

    def add_line_number(self) -> None:
        """
        Adds a line number in a span element
        """
        if self.file_length < 10:
            self.html += "<span class='line-number'>{}.</span>".format(self.line_number)
        elif self.file_length < 100:
            if self.line_number < 10:
                self.html += "<span class='line-number'>&nbsp;{}.</span>".format(self.line_number)
            else:
                self.html += "<span class='line-number'>{}.</span>".format(self.line_number)
        elif self.file_length < 1000:
            if self.line_number < 10:
                self.html += "<span class='line-number'>&nbsp;&nbsp;{}.</span>".format(self.line_number)
            elif self.line_number < 100:
                self.html += "<span class='line-number'>&nbsp;{}.</span>".format(self.line_number)
            else:
                self.html += "<span class='line-number'>{}.</span>".format(self.line_number)
        elif self.file_length < 10000:
            if self.line_number < 10:
                self.html += "<span class='line-number'>&nbsp;&nbsp;&nbsp;{}.</span>".format(self.line_number)
            elif self.line_number < 100:
                self.html += "<span class='line-number'>&nbsp;&nbsp;{}.</span>".format(self.line_number)
            elif self.line_number < 1000:
                self.html += "<span class='line-number'>&nbsp;{}.</span>".format(self.line_number)
            else:
                self.html += "<span class='line-number'>{}.</span>".format(self.line_number)

    def get_span_class(self, token: TokenInfo) -> Tuple:
        """
        Allocates the correct CSS class to a HTML span element
        represnting the current token

        Args:
            token (TokenInfo): the token to inspect
        """
        token_type = token_ids[token.type]
        token_value = token.string
        if token_type == "OP":
            return "python-op", None
        if token_type == "COMMENT":
            return "python-comment", None
        if token_type == "STRING":
            prefixed = self.has_str_prefix(token_value)
            return "python-str", prefixed
        if token_value in keywords:
            return "python-keyword", None
        if token_value in special_keywords:
            return "python-special-keyword", None
        return "python-var", None

    def has_str_prefix(self, value: str) -> bool:
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
        if value[0] in string_prefix or value[0] in bytes_prefix:
            return True
        return False

    def is_multi_line(self, value: str) -> bool:
        """
        Checks the starting character of the token value passed in
        to see if it a multi line string

        Args:
            value (str): string value of this token

        Returns:
            Boolean stating whether this is a multi line string
        """
        return value.startswith("\"\"\"") or value.startswith("'''")

    def delete_html(self) -> None:
        """
        Delete the last 2 lines added to the self.html string in
        the case that a multi-line string has been found. This
        stops nested code lines and allows the multi-line
        string to be added on separate lines, as it appears
        in the Python source code
        """
        last_code_line = self.html.rfind("<c")
        self.html = self.html[:last_code_line]
        self.line_number -= 1

    def handle_multi_line_str(self, value: str, spacer: str) -> None:
        """
        Create a series of code blocks represnting a multi-line
        string in the source code with preserved indentation

        Args:
            value (str): The string value to process
            spacer (str): amount of whitespace to add
        """
        first = True
        string_split = value.split("\n")
        for s in string_split:
            if first:
                total_spacer = spacer
                first = False
            else:
                whitespace = 0
                if len(s) > 0:
                    i = 0
                    while s[i].isspace():
                        whitespace += 1
                        i += 1
                total_spacer = "&nbsp;" * (whitespace - 1)
            self.html += "<code class=\"code-line\">"
            self.add_line_number()
            self.html += "<span class=\"python-str\">{x}{y}</span>".format(x=total_spacer, y=s)
            self.html += "</code>"
            self.line_number += 1

    def handle_string(self, value: str, prefixed: bool, spacer: str) -> bool:
        """
        Adds a string token to the HTML file by checking to
        see if the string has a prefix, is a multi-line string,
        or is just a regular string

        Args:
            value (str): token string value
            prefixed (bool): states whether the string is prefixed
            spacer (str): amount of whitespace to add
        """
        if prefixed:
            self.html += "<span class=\"python-str-prefix\">{spacer}{val}</span>".format(spacer=spacer, val=value[0])
            if self.is_multi_line(value[1:]):
                self.delete_html()
                self.handle_multi_line_str(value[1:], spacer)
                return True
            else:
                self.html += "<span class=\"python-str\">{spacer}{value}</span>".format(spacer=spacer, value=value)
                return False
        else:
            if self.is_multi_line(value):
                self.delete_html()
                self.handle_multi_line_str(value, spacer)
                return True
            else:
                self.html += "<span class=\"python-str\">{spacer}{value}</span>".format(spacer=spacer, value=value)
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
        self.html += "<span class=\"python-comment\">{spacer}{value}</span>".format(spacer=spacer, value=value)
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
        while True:

            token = next(self.tokens, None)

            if not token or token.type == "ENDMARKER":
                break

            if self.is_updated:
                token_type = token_ids_new[token.type]
            else:
                token_type = token_ids[token.type]

            token_value = token.string
            prev_token_start = None
            prev_token_length = None
            token_start = token.start[1]

            if token_type == "COMMENT":
                self.handle_comment(token_start, token_value)
                token = next(self.tokens, None)
                continue

            if token_type == "NL":
                self.handle_nl()
                continue

            if token_type == "INDENT" or token_type == "DEDENT":
                continue

            self.html += "<code class=\"code-line\">"
            self.add_line_number()
            first = True

            while token_type != "NEWLINE":

                if first:
                    spacer = "&nbsp;" * token_start
                    first = False
                else:
                    spacer = "&nbsp;" * (token_start - (prev_token_start + prev_token_length))

                span_class, prefixed = self.get_span_class(token)

                if token_type == "STRING":
                    break_parse = self.handle_string(token_value, prefixed, spacer)
                    if break_parse:
                        prev_token_start = token_start
                        prev_token_length = len(str(token_value))

                        token = next(self.tokens, None)

                        if not token or token_type == "ENDMARKER":
                            break

                        if self.is_updated:
                            token_type = token_ids_new[token.type]
                        else:
                            token_type = token_ids[token.type]

                        token_value = token.string
                        token_start = token.start[1]

                        break
                elif not prefixed:
                    self.html += "<span class=\"{span_class}\">{spacer}{token_value}</span>" \
                        .format(span_class=span_class,
                                spacer=spacer,
                                token_value=token_value)

                prev_token_start = token_start
                prev_token_length = len(str(token_value))

                token = next(self.tokens, None)

                if not token or token_type == "ENDMARKER":
                    break

                if self.is_updated:
                    token_type = token_ids_new[token.type]
                else:
                    token_type = token_ids[token.type]

                token_value = token.string
                token_start = token.start[1]

            self.html += "</code>"
            self.line_number += 1

    def add_html_meta(self) -> None:
        """
        Adds the metadata to the HTML string
        """
        self.html += """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Python HTML</title>
            <style>
                {}
            </style>
        </head>
        <body>
            <div class="code-block python-code-block">
        """.format(self.CSS)

    def close_html(self) -> None:
        """
        Adds the closing tags to the HTML string
        """
        self.html += """
            </div>
        </body>
        </html>
        """

    def generate_html(self) -> str:
        """
        Generates the HTML represention of the Python source
        code
        Returns:
            Value of self.html
        """
        self.add_html_meta()
        self.parse()
        self.close_html()
        return self.html

