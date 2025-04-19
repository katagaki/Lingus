from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from io import BytesIO
from os import listdir, makedirs, path
from pathlib import Path
from shutil import rmtree
from subprocess import run as run_subprocess
from tempfile import TemporaryDirectory
from traceback import format_exc

from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import ConversionResult
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode, TableStructureOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode
from docling_core.utils.file import DocumentStream

executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=5)

input_directory: str = "./docs"
output_directory: str = "./outputs"
pdf_directory_name: str = "pdf"
markdown_directory_name: str = "markdown"

rmtree(output_directory, ignore_errors=True)
makedirs(output_directory, exist_ok=True)
makedirs(path.join(output_directory, pdf_directory_name), exist_ok=True)
makedirs(path.join(output_directory, markdown_directory_name), exist_ok=True)


def filename(file_path: Path | str) -> str:
    if isinstance(file_path, Path):
        return path.splitext(path.basename(str(file_path)))[0]
    else:
        return path.splitext(path.basename(file_path))[0]


def convert_to_pdf(input_path: Path | str) -> bytes:
    # Clean up filename and ensure input_path is Path type
    if not isinstance(input_path, Path):
        input_path = Path(input_path)

    # Create temporary directories and run LibreOffice
    print(f"Converting {input_path} to PDF...")
    with TemporaryDirectory() as profile_directory, TemporaryDirectory() as output_directory:
        result = run_subprocess(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--nolockcheck",
                "--safe-mode",
                f"-env:UserInstallation=file://{profile_directory}",
                "--outdir",
                output_directory,
                str(input_path),
            ],
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        # Read converted PDF
        if result.returncode == 0:
            output_path: str = path.join(output_directory, filename(input_path) + ".pdf")
            if path.exists(output_path):
                pdf_bytes: bytes = Path(output_path).read_bytes()
                save_to_file(pdf_bytes, path.join(pdf_directory_name, filename(input_path) + ".pdf"))
                return pdf_bytes
            else:
                raise FileNotFoundError(f"Converted PDF file not found: {output_path}")
        else:
            raise RuntimeError(f"{result.stderr} ({result.returncode})")


def convert_to_markdown(file_path: str, input_pdf: bytes) -> str:
    # Read file into stream
    stream: DocumentStream = DocumentStream(name=filename(file_path), stream=BytesIO(input_pdf))

    # Convert to Markdown using Docling
    converter: DocumentConverter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=PdfPipelineOptions(
                    do_table_structure=True,
                    do_ocr=False,
                    table_structure_options=TableStructureOptions(
                        do_cell_matching=True,
                        mode=TableFormerMode.ACCURATE,
                    ),
                    generate_page_images=True,
                    generate_picture_images=True
                )
            )
        }
    )
    result: ConversionResult = converter.convert(stream)
    markdown: str = result.document.export_to_markdown(
        image_mode=ImageRefMode.REFERENCED
    )
    save_to_file(markdown, path.join(markdown_directory_name, filename(file_path) + ".md"))

    return markdown


def save_to_file(content: str | bytes, file_path: str):
    if isinstance(content, str):
        with open(path.join(output_directory, file_path), "w") as output_file:
            output_file.write(content)
    elif isinstance(content, bytes):
        with open(path.join(output_directory, file_path), "wb") as output_file:
            output_file.write(content)
    else:
        raise RuntimeError(f"Unsupported content type: {type(content)}")


def convert_to_pdf_then_markdown(input_filename: str) -> str:
    time_started: datetime = datetime.now()
    try:
        print(f"Converting {input_filename} to PDF...")
        pdf_bytes: bytes = convert_to_pdf(path.join(input_directory, input_filename))
        print(f"Converted {input_filename} to PDF: {len(pdf_bytes)} bytes")

        print(f"Converting {len(pdf_bytes)} bytes to Markdown...")
        markdown_string: str = convert_to_markdown(input_filename, pdf_bytes)
        print(f"Converted {len(pdf_bytes)} bytes to Markdown: {len(markdown_string)} characters")

        output_string = markdown_string

    except Exception as e:
        output_string = f"Failed to convert {input_filename} to PDF: {e}\n{format_exc()}"

    time_ended: datetime = datetime.now()
    output_string += (f"\n\n----- Time taken: "
                      f"{(time_ended - time_started).seconds // 60} minutes "
                      f"{(time_ended - time_started).seconds % 60} seconds -----")

    return output_string


if __name__ == "__main__":
    input_filenames: list[str] = listdir(input_directory)
    for input_filename in input_filenames:
        executor.submit(convert_to_pdf_then_markdown, input_filename)
