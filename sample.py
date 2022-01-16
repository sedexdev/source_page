#!/usr/bin/bash python


def pytml(is_awesome) -> str:
    if is_awesome:
        return f"Pytml is awesome!"
    return f"Pytml is still awesome!"


if __name__ == "__main__":
    pytml(True)

