import sys
import os
from datetime import datetime


def prompt_for_content() -> list[str]:
    content_lines = []
    while True:
        line = input("Enter content line: ")
        if line.lower() == "stop":
            break
        content_lines.append(line)
    return content_lines


def create_directory(path_parts: list[str]) -> str:
    try:
        directory_path = os.path.join(*path_parts)
        os.makedirs(directory_path, exist_ok=True)
        return directory_path
    except PermissionError:
        print("Permission denied: unable to create directory.")
    except Exception as e:
        print(f"An error occurred creating "
              f"directory: {e}")


def create_file(file_name: str, directory: str = None) -> None:
    try:
        if directory:
            file_path = os.path.join(directory, file_name)
        else:
            file_path = file_name

        content_lines = prompt_for_content()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(file_path, "w") as file:
            file.write(timestamp + "\n")
            for idx, line in enumerate(content_lines, start=1):
                file.write(f"{idx} {line}\n")

        print(f"File {file_name} created")
    except PermissionError:
        print("Permission denied: unable to create or write to file.")
    except Exception as e:
        print(f"An error occurred creating or "
              f"writing to file: {e}")


def main() -> None:
    try:
        args = sys.argv[1:]

        if "-d" in args and "-f" in args:

            dir_index = args.index("-d") + 1
            file_index = args.index("-f") + 1

            if args.index("-d") > args.index("-f"):
                dir_index, file_index = file_index, dir_index

            dir_start = dir_index
            if "-f" in args[dir_index:]:
                dir_end = args.index("-f", dir_index)
            else:
                dir_end = None

            directory_args = args[dir_start:dir_end]
            directory = create_directory(directory_args)
            if directory:
                create_file(args[file_index], directory)
        elif "-d" in args:
            create_directory(args[args.index("-d") + 1:])
        elif "-f" in args:
            create_file(args[args.index("-f") + 1])
        else:
            raise ValueError("Invalid usage.")
    except ValueError as e:
        print(e)
        print("Usage: create_file.py -d [directory path parts] -f [file name]")
        print("Or: create_file.py -d [directory path parts]")
        print("Or: create_file.py -f [file name]")


if __name__ == "__main__":
    main()
