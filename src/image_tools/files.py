from os import scandir
from pathlib import Path


def list_all_files_recursively(dir_path: "Path"):
    files = scandir(dir_path)
    for file in files:
        file_path = Path(file.path)
        if file.is_dir:
            yield from list_all_files_recursively(file_path)
        if file.is_file:
            yield file_path
