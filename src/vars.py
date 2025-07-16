"""
Tokens and theme variable module
"""

import token
import tokenize

# Merge both token and tokenize integer constants into a single mapping
token_map = {}

# From `token` module
token_map.update({
    value: name
    for name, value in vars(token).items()
    if isinstance(value, int)
})

# From `tokenize` module (these may overwrite or add to the above)
token_map.update({
    value: name
    for name, value in vars(tokenize).items()
    if isinstance(value, int)
})

keywords = [
    "True",
    "False",
    "None",
    "def",
    "nonlocal",
    "lambda",
    "async"]

special_keywords = [
    "in",
    "is",
    "and",
    "or",
    "not",
    "await",
    "from",
    "import",
    "as",
    "pass",
    "break",
    "continue",
    "return",
    "try",
    "except",
    "finally",
    "raise",
    "class",
    "for",
    "while",
    "assert",
    "del",
    "global",
    "with",
    "if",
    "else",
    "elif",
    "yield"]

theme_list = [
    "cool_blue_light",
    "cyber",
    "robot",
    "robot_light"
]
