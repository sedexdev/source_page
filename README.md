# SourcePage: A Python parser that creates HTML pages

Parses Python source code and produces a pretty-printed, syntax-highlighted HTML representation of the code. This tool uses
the <a href="https://docs.python.org/3/library/tokenize.html">tokenize</a> built-in Python tokenizer class for lexical analysis, 
then parses the tokens to generate the HTML output.

# Usage

<code>python main.py [-h] -p [abspath]/python_script.py [-t] [THEME_NAME] [-o]</code>

This will create well-formatted HTML from the Python script that is sent to <b>stdout</b> by default.

The output can easily be sent to a file called <code>output.html</code> by using the <code>-o</code> switch.
The HTML file will be saved in your current working directory.

<b>NOTE</b>: This program requires <b>Python3.6</b> or later.

# Options

<code>-h, --help</code>: Show the options
</br>
<code>-p, --path</code>: The absolute or relative path to the Python source file to parse (**required**)
</br>
<code>-t, --theme</code>: The syntax highlighting theme</code>
</br>
<code>-o, --output</code>: Send output to a file rather than stdout
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

# Binary Files

Binaries are available for Linux and Windows from the <a href="https://github.com/sedexdev/source_page/tree/master/source_page/bin">bin</a> folder.

These were compiled using <a href="https://pyinstaller.readthedocs.io/en/stable/">Pyinstaller</a>. This tool bundles
application modules and libraries into a single executable that <b>doesn't require Python</b> to be installed on your system
to run.

The platforms used to compile the executables were:

<b>Linux:</b> Linux Mint 20.2 Uma. Linux version 5.4.0-97-generic
</br>
<b>Windows:</b> Windows 10

# License

<a href="https://github.com/sedexdev/source_page/blob/master/LICENSE">M.I.T</a>
