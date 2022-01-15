# Python HTML Parser

Parses Python source code and produces a colour-coded HTML representation of the code. 
This app uses the <a href="https://docs.python.org/3/library/tokenize.html">tokenize</a> 
built-in Python tokenizer class for lexical analysis, then parses the tokens to generate 
the HTML output.

# Usage

<code>python main.py -p [abspath]/python_script.py</code>

This will create a pretty-printed, colour coded HTML file of the Python script that you
can add to a Web page.

The HTML file will be saved in the current working directory.

<b>NOTE</b>: This program requires <b>Python3.6</b> or later 

In time this app should be available on <a href="https://pypi.org/">PyPI</a>

# License

<a href="https://github.com/sedexdev/python_html_parser/blob/main/LICENSE">M.I.T</a>
