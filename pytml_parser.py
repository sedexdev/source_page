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

    def __init__(self, tokens: Iterable, is_updated: bool) -> None:
        """
        Constructor for the PythonParser class
        Args:
            tokens (Iterable): a list of tokens
            is_updated (bool): states if Python version is using
                               an updated token ID dictionary
        """
        self.tokens = tokens
        self.is_updated = is_updated
        self.html = ""
        self.line_number = 1

    def has_str_prefix(self, value: str, spacer: str) -> bool:
        """
        Inspect a token value of type string to check if it has a
        prefix or contains escaped characters.
        Args:
            value (str): the string value of this token
            spacer (str): whitespace to add to the span element
        Returns:
            Boolean defining whether a string prefix has been added
        """
        updated = False
        if value[0] in ["r", "u", "R", "U", "f", "F", "fr", "Fr", "fR", "FR",
                        "rf", "rF", "Rf", "RF", "b", "B", "br", "Br", "bR",
                        "BR", "rb", "rB", "Rb", "RB"]:
            self.html += f"<span class=\"python-str-prefix\">{spacer}{value[0]}</span>"
            self.html += f"<span class=\"python-str\">{value[1:]}</span>"
            updated = True
        return updated

    def get_span_class(self, token: TokenInfo, spacer: str) -> Tuple:
        """
        Allocates the correct CSS class to a HTML span element
        represnting the current token
        Args:
            token (TokenInfo): the token to inspect
            spacer (str): whitespace to add to a span element
        """
        token_type = token_ids[token.type]
        token_value = token.string
        if token_type == "OP":
            return "python-op", None
        if token_type == "COMMENT":
            return "python-comment", None
        if token_type == "STRING":
            updated = self.has_str_prefix(token_value, spacer)
            return "python-str", updated
        if token_value in keywords:
            return "python-keyword", None
        if token_value in special_keywords:
            return "python-special-keyword", None
        return "python-var", None

    def add_line_number(self) -> None:
        """
        Adds a line number in a span element
        """
        if self.line_number < 10:
            self.html += f"<span class='line-number'>&nbsp;{self.line_number}. </span>"
        else:
            self.html += f"<span class='line-number'>{self.line_number}. </span>"

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

                span_class, updated = self.get_span_class(token, spacer)
                if not updated:
                    self.html += f"<span class=\"{span_class}\">{spacer}{token_value}</span>"
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
        self.html += f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Python HTML</title>
            <style>
                {self.CSS}
            </style>
        </head>
        <body>
            <div class="code-block python-code-block">
        """

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

