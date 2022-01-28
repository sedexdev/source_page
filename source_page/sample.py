#!/usr/bin/bash python


def source_page(is_awesome) -> str:
    """
    Returns an awesome string

    Args:
        is_awesome (bool): is SourcePage awesome?
    """
    if is_awesome:
        return f"{is_awesome}! SourcePage is awesome!"
    return f"{is_awesome}! Nah, SourcePage is still awesome!"


if __name__ == "__main__":
    source_page_is_awesome = source_page(True)
    print(source_page_is_awesome)
