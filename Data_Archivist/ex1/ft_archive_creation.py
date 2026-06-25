import sys
import typing


def ft_archive_creation() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    try:
        print("=== Cyber Archives Recovery & Preservation ===")
        book: typing.IO[str] = open(sys.argv[1], "r")
        r = book.read()
        print(f"Accessing file ’{sys.argv[1]}’")
        print("---\n")
        print(r)
        print("---\n")
        book.close()
        print(f"File ’{sys.argv[1]}’ closed.")
        print("Transform data:\n---\n")
        new_book: typing.IO[str] = open(sys.argv[1], "r")
        w = new_book.read()
        txt = ""
        for char in w:
            if char == "\n":
                char = "#"
                txt += char
                txt += "\n"
            else:
                txt += char
        txt += "#\n"
        print(txt)
        print("\n---")
        filenmae = input("Enter new file name (or empty):")
        if len(filenmae) == 0:
            print("Not saving data.")
            return
        new_txt: typing.IO[str] = open(filenmae, "w")
        new_txt.write(txt)
        print(f"Saving data to ’{filenmae}’")
        print(f"Data saved in file ’{filenmae}’.")
        new_txt.close()
    except Exception as error:
        print(f"Accessing file ’{sys.argv[1]}’")
        print(f"Error opening file ’{sys.argv[1]}’: {error}")


if __name__ == "__main__":
    ft_archive_creation()
