# 📘 SourcePage: Parse Python source to HTML

Parses Python source code and produces a pretty-printed, syntax-highlighted HTML representation of the code. This tool uses
the [tokenize](https://docs.python.org/3/library/tokenize.html) built-in Python tokenizer class for lexical analysis,
then parses the tokens to generate the HTML output.

## ✨ Features

-   ✅ Pretty printed Python to add to your Web page
-   ✅ Line numbering
-   ✅ Syntax highlighting
-   📦 Easy to install and use
-   🔧 Customisable themes - easily extend by creating additional CSS blocks in `themes.py`

## 🚀 Demo

Sample using built in theme 'CYBER'

![Sample HTML Output](/src/imgs/sample.png)

## 📦 Installation

### Prerequisites

```bash
Python >= 3.6
```

### Get the code

```bash
# Clone the repository
git clone https://github.com/sedexdev/source_page.git
cd source_page
```

## 🛠️ Usage

`python3 src/main.py [-h] -p /path/to/script.py [-t] [THEME_NAME] [-o]`

-   This will create well-formatted HTML from the Python script that is sent to `stdout` by default.
-   Using the `-o` switch creates a file called `output.html` in the current directory.

_NOTE_: This program requires **Python3.6** or later.

### Options

-   `-h, --help`: Show the options
-   `-p, --path`: The absolute or relative path to the Python source file to parse (**required**)
-   `-t, --theme`: The syntax highlighting theme`
-   `-o, --output`: Send output to a file rather than stdout

### Available Themes:

-   COOL_BLUE (default)
-   COOL_BLUE_LIGHT
-   CYBER
-   ROBOT
-   ROBOT_LIGHT

## 📂 Project Structure

```
source_page/
│
├── src/                # Source files
├── .gitignore          # Git ignore file
├── LICENSE             # MIT License file
└── README.md           # This README.md file
```

## 🐛 Reporting Issues

Found a bug or need a feature? Open an issue [here](https://github.com/sedexdev/source_page/issues).

## 🧑‍💻 Authors

-   **Andrew Macmillan** – [@sedexdev](https://github.com/sedexdev)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/sedexdev/source_page/blob/master/LICENSE) file for details.
