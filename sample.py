#!/usr/bin/bash python


def pytml(is_awesome) -> str:
    """
    Returns an awesome string

    Args:
        is_awesome (bool): is Pytml awesome?
    """
    if is_awesome:
        return f"{is_awesome}! Pytml is awesome!"
    return f"{is_awesome}! Nah, Pytml is still awesome!"


if __name__ == "__main__":
    pytml_is_awesome = pytml(True)
    print(pytml_is_awesome)
