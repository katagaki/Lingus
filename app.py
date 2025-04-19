from concurrent.futures import Future
from os import listdir

from lingus import input_directory, executor
from lingus.conversion import convert_to_pdf_then_markdown
from lingus.files import cleanup_files

if __name__ == "__main__":
    cleanup_files()
    input_filenames: list[str] = listdir(input_directory)
    futures: list[Future] = [
        executor.submit(convert_to_pdf_then_markdown, input_filename)
        for input_filename in input_filenames
    ]
    for future in futures:
        future.result()
