import sys
import typing


def ft_ancient_text() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    try:
        print("=== Cyber Archives Recovery ===")
        book: typing.IO[str] = open(sys.argv[1])
        r = book.read()
        print(f"Accessing file ’{sys.argv[1]}’")
        print("---\n")
        print(r)
        print("\n---")
        book.close()
        print(f"File ’{sys.argv[1]}’ closed.")
    except Exception as error:
        print(f"Accessing file ’{sys.argv[1]}’")
        print(f"Error opening file ’{sys.argv[1]}’: {error}")


if __name__ == "__main__":
    ft_ancient_text()
