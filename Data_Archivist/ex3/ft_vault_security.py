import sys


def secure_archive(file: str, action: str, message: str) -> tuple[bool, str]:
    try:
        if action == "r":
            with open(file, action) as file_name:
                r = file_name.read()
                return (True, r)
        elif action == "w":
            with open(file, action) as file_name:
                file_name.write(message)
                return (True, str("Content successfully written to file"))
        return (False, "Invalid action")
    except Exception as error:
        return (False, str(error))


def main() -> None:
    print("=== Cyber Archives Security ===\n")
    if len(sys.argv) == 1:
        print("not found data :(")
        return
    re_1 = "anyfile.txt"
    success1, message1 = secure_archive(re_1, "r", "wellcome my zone")
    print(f"Using ’{re_1}’ to read from a nonexistent file:")
    print(f"({success1}, '{message1}')\n")
    re_2 = "/etc/master.passwd"
    success2, message2 = secure_archive(re_2, "r", "wellcome my zone")
    print(f"Using ’{re_2}’ to read from an inaccessible file:")
    print(f"({success2}, '{message2}')\n")
    success3, message3 = secure_archive(sys.argv[1], "r", "wellcome my zone")
    print(f"Using ’{sys.argv[1]}’ to read previous content to a new file:")
    print(f"({success3}, '{message3}')\n")
    success4, message4 = secure_archive(sys.argv[1], "w", "wellcome my zone")
    print(f" Using ’{sys.argv[1]}’ to write previous content to a new file:")
    print(f"({success4},'{message4}')")


if __name__ == "__main__":
    main()
