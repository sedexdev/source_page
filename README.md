# Python HTML Parser

Parses Python source code and produces a colour-coded HTML representation of the code. This app uses
the <a href="https://docs.python.org/3/library/tokenize.html">tokenize</a>
built-in Python tokenizer class for lexical analysis, then parses the tokens to generate the HTML output.

# Usage

<code>python main.py -p [abspath]/python_script.py [-t] [THEME_NAME] [-o]</code>

This will create a pretty-printed, colour coded HTML file of the Python script that you can add to a Web page.

The HTML file will be saved in the current working directory.

<b>NOTE</b>: This program requires <b>Python3.6</b> or later

# Options

<code>-h</code>: Show the options
</br>
<code>-p, --path</code>: The absolute path of the Python source file to parse (**required**)
</br>
<code>-t, --theme</code>: The syntax highlighting theme</code>
</br>
<code>-o, --out</code>: Send output to stdout rather than a file
</br></br>
Available Themes:
<ul>
    <li>COOL_BLUE (default)</li>
    <li>COOL_BLUE_LIGHT </li>
    <li>CYBER </li>
    <li>ROBOT </li>
    <li>ROBOT_LIGHT </li>
</ul>

# Sample Output

Sample using default theme 'COOL_BLUE'

![Sample HTML Output](/source_page/imgs/sample.png)

# License

<a href="https://github.com/sedexdev/python_html_parser/blob/main/LICENSE">M.I.T</a>
