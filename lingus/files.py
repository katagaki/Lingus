from os import path, makedirs
from pathlib import Path
from shutil import rmtree

from lingus import output_directory, pdf_directory_name, markdown_directory_name


def filename(file_path: Path | str) -> str:
    if isinstance(file_path, Path):
        return path.splitext(path.basename(str(file_path)))[0]
    else:
        return path.splitext(path.basename(file_path))[0]


def save_to_file(content: str | bytes, file_path: str):
    if isinstance(content, str):
        with open(path.join(output_directory, file_path), "w") as output_file:
            output_file.write(content)
    elif isinstance(content, bytes):
        with open(path.join(output_directory, file_path), "wb") as output_file:
            output_file.write(content)
    else:
        raise RuntimeError(f"Unsupported content type: {type(content)}")

def cleanup_files():
    rmtree(output_directory, ignore_errors=True)
    makedirs(output_directory, exist_ok=True)
    makedirs(path.join(output_directory, pdf_directory_name), exist_ok=True)
    makedirs(path.join(output_directory, markdown_directory_name), exist_ok=True)
