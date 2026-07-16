import sys
import typing


def ft_stream_management() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    try:
        print("=== Cyber Archives Recovery & Preservation ===")
        txt: typing.IO[str] = open(sys.argv[1], "r")
        r = txt.read()
        print(f"Accessing file ’{sys.argv[1]}’\n---\n")
        sys.stdout.write(r)
        sys.stdout.flush()
        txt.close()
        print(f"\n\n---\nFile ’{sys.argv[1]}’ closed.\n")
        print("Transform data:\n---\n")
        txt_txt: typing.IO[str] = open(sys.argv[1], "r")
        new_txt = ""
        w = txt_txt.read()
        for char in w:
            if char == "\n":
                char = "#\n"
                new_txt += char
            else:
                new_txt += char
        new_txt += "#\n"
        txt_txt.close()
        sys.stdout.write(new_txt)
        sys.stdout.flush()
        print("\n---")
        sys.stdout.write("Enter new file name (or empty): ")
        sys.stdout.flush()
        filename = sys.stdin.readline()
        if len(filename) == 1:
            sys.stdout.write("Not saving data.\n")
            sys.stdout.flush()
            return
        try:
            filename_af_eddite = ""
            for ad in filename:
                if ad != "\n":
                    filename_af_eddite += ad
            book: typing.IO[str] = open(filename_af_eddite, "w")
            book.write(new_txt)
            book.close()
            print(f"Saving data to ’{filename_af_eddite}’")
            print(f"Data saved in file ’{filename_af_eddite}’.")
        except Exception as error:
            sys.stdout.write(f"Saving data to '{filename_af_eddite}'\n")
            print(
                "[STDERR] Error opening file "
                f"’{filename_af_eddite}’: {error}"
            )
            print("Data not saved.")
    except Exception as error:
        sys.stderr.write(f"Accessing file ’{sys.argv[1]}’\n")
        sys.stderr.write(
            "[STDERR] "
            f"Error opening file ’{sys.argv[1]}’: {error}\n"
        )


if __name__ == "__main__":
    ft_stream_management()
