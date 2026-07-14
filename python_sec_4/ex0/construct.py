import sys
import site
import os


def in_out_virtual() -> None:
    if sys.prefix == sys.base_prefix:
        print(
            "# Should detect no virtual environment"
            " and provide instructions"
        )
    else:
        print("# Should detect virtual environment and show details")


def The_Matrix() -> None:
    if sys.prefix == sys.base_prefix:
        print("MATRIX STATUS: You’re still plugged in\n")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected\n")
        print(
            "WARNING: You’re in the global environment!\n"
            "The machines can see everything you install.\n"
        )
        print(
            "To enter the construct, run:\n"
            "python -m venv matrix_env\n"
            "source matrix_env/bin/activate # On Unix\n"
            "matrix_env\\Scripts\\activate # On Windows\n"
        )
        print("Then run this program again.")
    else:
        print("MATRIX STATUS: Welcome to the construct\n")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}\n")
        print(
            "SUCCESS: You’re in an isolated environment!\n"
            "Safe to install packages without affecting\n"
            "the global system.\n"
        )
        print(f"Package installation path:\n{site.getsitepackages()[1]}")


if __name__ == "__main__":
    in_out_virtual()
    The_Matrix()
