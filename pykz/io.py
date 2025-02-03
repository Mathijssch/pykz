"""Reading and writing to files.
"""

from __future__ import annotations

import os
from typing import Any


def __export_to_tempfile(code: str) -> str:
    """Export latex code to temp file"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        print("Writing to tempfile")
        f.write(code)
        # f.flush()
    return f.name


def export_pdf_from_code(code: str) -> str:
    """
    Compile the given ``tex`` code to a pdf file.

    Use ``pdflatex`` to compile the document to a standalone pdf file.

    Parameters
    ----------
    code
        String representation of the tex to be compiled.

    Returns
    -------
    str
        Path to the generated pdf file.
    """
    file = __export_to_tempfile(code)
    return export_pdf_from_file(file)


def export_pdf_from_file(path: str) -> str:
    """
    Compile the ``tex`` code at the given path.


    Use ``pdflatex`` to compile the document to a standalone pdf file.

    Parameters
    ----------
    path
        The path to the ``tex`` code to be compiled.

    Returns
    -------
    str
        The path to the generated pdf file.

    Raises
    ------
    PDFlatexNotFoundError:
        If pdflatex is not installed.
    CompilationError:
        If the given document could not be compiled by pdflatex.
    """
    import subprocess
    from .exceptions import PDFlatexNotFoundError, CompilationError
    import os
    working_dir = os.path.dirname(path)

    options: dict[str, Any] = dict(capture_output=True, check=True)
    if working_dir:
        options["cwd"] = working_dir

    try:
        import shutil
        pdflatex_path = shutil.which('pdflatex')
        if pdflatex_path is None:
            raise PDFlatexNotFoundError(f"Could not find executable `pdflatex` to compile {path}. Please make sure it is installed and accessible in the system's path.")

        subprocess.run([pdflatex_path, "-interaction=nonstopmode", "-halt-on-error", path], **options)
        # print("Pdflatex done!")
    except subprocess.CalledProcessError as e:
        error_message = f"{e.stdout.decode('UTF-8')}\n\nCompilation failed with the error above ☝️ "
        raise CompilationError(error_message)
    import os

    basename = os.path.splitext(path)[0]
    for ext in {".aux", ".log"}:
        try:
            os.remove(basename + ext)
        except FileNotFoundError:
            ...
    return f"{basename}.pdf"


def export_png_from_file(input_file: str, **options) -> str:
    """
    Export the given tex file to a png image.

    The tex file is first compiled to pdf using pdflatex. Then the
    resulting pdf is converted to an image using ``pdf2image``.

    Parameters
    ----------
    input_file
        The path to the ``tex`` code to be compiled.

    Returns
    -------
    str
        The path to the generated png file.
    """
    import pdf2image
    pdf_file = export_pdf_from_file(input_file)
    path = pdf_file.replace(".pdf", ".png")
    options["output_file"] = path
    pdf2image.convert_from_path(pdf_file, **options)
    return path


def export_png_from_code(code: str, path: str, **options):
    """
    Export the given tex file to a png image.

    The tex file is first compiled to pdf using pdflatex. Then the
    resulting pdf is converted to an image using ``pdf2image``.

    Parameters
    ----------
    input_file
        The path to the ``tex`` code to be compiled.

    Returns
    -------
    str
        The path to the generated png file.
    """
    import pdf2image
    pdf_file = export_pdf_from_code(code)
    options["output_file"] = path
    pdf2image.convert_from_path(pdf_file, **options)


def open_pdf_file(file_path: str):
    """
    Open the pdf file at the given path in the system default pdf reader.

    Parameters
    ----------
    file_path
        Path to the pdf file to open.
    """
    import sys
    import subprocess
    print("Opening pdf file")

    if sys.platform.startswith('darwin'):  # macOS
        result = subprocess.run(['open', file_path], capture_output=True, text=True)
    elif sys.platform.startswith('win32'):  # Windows
        import os
        result = os.startfile(file_path)
    elif sys.platform.startswith('linux'):  # Linux
        result = subprocess.run(['xdg-open', file_path], capture_output=True, text=True)
    else:
        print("Unsupported platform. Unable to open PDF file.")
    input("Press any key to continue.")
    if result.returncode != 0:
        print(sys.stdout)


def preview_latex_doc(code: str) -> str:
    """
    Preview the given tex code.

    The given code must be a valid tex document that can be compiled.
    It gets compiled to a temporary file and then opened in the default pdf reader.

    Parameters
    ----------
    code
        The tex to be compiled.

    Returns
    -------
    str
        The path to which the compiled pdf was written. Could be useful for cleanup.
    """
    pdf_path = export_pdf_from_code(code)
    print(pdf_path)

    try:
        open_pdf_file(pdf_path)
    except Exception as e:
        try:
            os.remove(pdf_path)
        except FileNotFoundError():
            ...
        raise e


if __name__ == "__main__":

    TEX_STRING = r"""
    \documentclass{article}
    \begin{document}
        hello world.
    \end{document}
    """
    preview_latex_doc(TEX_STRING)
