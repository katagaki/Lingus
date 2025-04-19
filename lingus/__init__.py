from concurrent.futures import ThreadPoolExecutor
from os import environ, makedirs, path
from shutil import rmtree

executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=int(environ.get("WORKER_LIMIT", "4")))

input_directory: str = f"./{environ.get('INPUT_DIRECTORY', 'docs')}"
output_directory: str = f"./{environ.get('OUTPUT_DIRECTORY', 'outputs')}"
pdf_directory_name: str = "pdf"
markdown_directory_name: str = "markdown"

makedirs(output_directory, exist_ok=True)
makedirs(path.join(output_directory, pdf_directory_name), exist_ok=True)
makedirs(path.join(output_directory, markdown_directory_name), exist_ok=True)
