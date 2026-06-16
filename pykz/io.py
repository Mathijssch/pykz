"""Reading and writing to files."""

from __future__ import annotations

import os
from typing import Any, Sequence, Type
from pathlib import Path
from .exceptions import (
    PDFlatexNotFoundError,
    CompilationError,
    OpenPdfException,
    WrapperError,
)

Pathlike = str | Path


def __export_to_tempfile(code: str) -> str:
    """Export latex code to temp file"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        print("Writing to tempfile")
        f.write(code)
        # f.flush()
    return f.name


def export_pdf_from_code(code: str, cmd: str = "pdflatex", cmd_args: Sequence[str] | None = None) -> Path:
    """
    Compile the given ``tex`` code to a pdf file.

    Use ``pdflatex`` or the specified command to compile the document to a
    standalone pdf file.

    Parameters
    ----------
    code
        String representation of the tex to be compiled.
    cmd
        The command to use for compilation. E.g. ``pdflatex``, ``lualatex``,
        or ``xelatex``.
    cmd_args
        Additional command line arguments to pass to the compilation command.
        Defaults to ``['-interaction=nonstopmode', '-halt-on-error']``.

    Returns
    -------
    Path
        Path to the generated pdf file.
    """
    file = __export_to_tempfile(code)
    return export_pdf_from_file(file, cmd=cmd, cmd_args=cmd_args)


def export_pdf_from_file(
    path: Pathlike, cmd: str = "pdflatex", cmd_args: Sequence[str] | None = None
) -> Path:
    """
    Compile the ``tex`` code at the given path.


    Use ``pdflatex`` or the specified command to compile the document to a
    standalone pdf file.

    Parameters
    ----------
    path
        The path to the ``tex`` code to be compiled.
    cmd
        The command to use for compilation. E.g. ``pdflatex``, ``lualatex``,
        or ``xelatex``.
    cmd_args
        Additional command line arguments to pass to the compilation command.
        Defaults to ``["-interaction=nonstopmode", "-halt-on-error"]``.

    Returns
    -------
    Path
        The path to the generated pdf file.

    Raises
    ------
    PDFlatexNotFoundError:
        If the specified compilation command is not found.
    CompilationError:
        If the given document could not be compiled by the specified command.
    """

    path = Path(path)
    working_dir = path.parent
    if cmd_args is None:
        cmd_args = ["-interaction=nonstopmode", "-halt-on-error"]

    options: dict[str, Any] = dict(capture_output=True, check=True)
    if working_dir:
        options["cwd"] = working_dir

        import shutil

        cmd_path = shutil.which(cmd)
        if cmd_path is None:
            raise PDFlatexNotFoundError(
                f"Could not find executable `{cmd}` to compile {path}. Please make sure it is installed and accessible in the system's path."
            )

        _subprocess(
            [cmd_path, *cmd_args, str(path)],
            CompilationError,
        )
    import os

    for ext in {".aux", ".log"}:
        try:
            aux_file_path = path.with_suffix(ext)
            print(f"Removing {aux_file_path}")
            os.remove(aux_file_path)
        except FileNotFoundError:
            ...
    return path.with_suffix(".pdf")


def export_png_from_file(input_file: Pathlike, cmd: str = "pdflatex", cmd_args: Sequence[str] | None = None, **options) -> Path:
    """
    Export the given tex file to a png image.

    The tex file is first compiled to pdf using the specified command. Then the
    resulting pdf is converted to an image using ``pdf2image``.

    Parameters
    ----------
    input_file
        The path to the ``tex`` code to be compiled.
    cmd
        The command to use for compilation. E.g. ``pdflatex``, ``lualatex``,
        or ``xelatex``.
    cmd_args
        Additional command line arguments to pass to the compilation command.
        Defaults to ``['-interaction=nonstopmode', '-halt-on-error']``.

    Returns
    -------
    Path
        The path to the generated png file.
    """
    pdf_file = export_pdf_from_file(input_file, cmd=cmd, cmd_args=cmd_args)
    output_path = pdf_file.with_suffix(".png")
    return __convert_pdf_to_png(pdf_file, output_path, **options)


def export_png_from_code(code: str, path: str, cmd: str = "pdflatex", cmd_args: Sequence[str] | None = None, **options):
    """
    Export the given tex file to a png image.

    The tex file is first compiled to pdf using the specified command. Then the
    resulting pdf is converted to an image using ``pdf2image``.

    Parameters
    ----------
    code
        String representation of the tex to be compiled.
    path
        The output path for the png file.
    cmd
        The command to use for compilation. E.g. ``pdflatex``, ``lualatex``,
        or ``xelatex``.
    cmd_args
        Additional command line arguments to pass to the compilation command.
        Defaults to ``['-interaction=nonstopmode', '-halt-on-error']``.

    Returns
    -------
    Path
        The path to the generated png file.
    """
    pdf_file = export_pdf_from_code(code, cmd=cmd, cmd_args=cmd_args)
    output_path = str(path)
    return __convert_pdf_to_png(pdf_file, output_path, **options)


def __convert_pdf_to_png(
    pdf_file: Pathlike, output_file: Pathlike | None = None, **options
):
    try:
        import pdf2image
    except ImportError:
        raise RuntimeError(
            "Exporting to png relies on the dependency pdf2image. Install it using `pip install pdf2image`, or install pykz using `pip install pykz[png]`"
        )

    pdf_file = Path(pdf_file)
    output_file = (
        pdf_file.with_suffix(".png") if output_file is None else Path(output_file)
    )
    default_options = {
        "output_file": output_file,
        "single_file": True,
        "transparent": True,
    }
    default_options.update(options)
    images = pdf2image.convert_from_path(pdf_file, **default_options)
    for image in images:
        image.save(output_file)
    return output_file


def _subprocess(cmds: list[str], exception_cls: Type[WrapperError], **options):
    import subprocess

    default_options: dict[str, Any] = dict(capture_output=True, check=True)
    default_options.update(options)
    try:
        result = subprocess.run(cmds, **options)
    except subprocess.CalledProcessError as e:
        raise exception_cls(e)
    return result


def open_pdf_file(file_path: str):
    """
    Open the pdf file at the given path in the system default pdf reader.

    Parameters
    ----------
    file_path
        Path to the pdf file to open.
    """
    import sys

    print(f"Opening pdf file {file_path} ...")

    if sys.platform.startswith("darwin"):  # macOS
        _subprocess(["open", file_path], OpenPdfException)
    elif sys.platform.startswith("win32"):  # Windows
        import os

        os.startfile(file_path)
    elif sys.platform.startswith("linux"):  # Linux
        _subprocess(["xdg-open", file_path], OpenPdfException)
    else:
        print("Unsupported platform. Unable to open PDF file.")
    input("Press any key to continue.")


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
            print(f"Removing {pdf_path}")
            os.remove(pdf_path)
        except FileNotFoundError:
            print(f"Could not remove {pdf_path}. File not found.")
        raise e
    try:
        print(f"Removing {pdf_path}")
        os.remove(pdf_path)
    except FileNotFoundError:
        print(f"Could not remove {pdf_path}. File not found.")


if __name__ == "__main__":
    TEX_STRING = r"""
    \documentclass{article}
    \begin{document}
        hello world.
    \end{document}
    """
    preview_latex_doc(TEX_STRING)
