import subprocess


class WrapperError(Exception):
    cmd_name = "Subprocess"

    def __init__(self, parent: Exception, *options):
        message = f"{self._decode_message(parent)}\n\{self.cmd_name} failed with the error above ☝️ "
        super().__init__(message, *options)

    def _decode_message(self, error: Exception) -> str:
        return error.message


class CompilationError(WrapperError):
    cmd_name = "Compilation"

    def _decode_message(self, e: subprocess.CalledProcessError):
        return e.stdout.decode("UTF-8")


class OpenPdfException(WrapperError):
    cmd_name = "Opening PDF"

    def _decode_message(self, e: subprocess.CalledProcessError):
        return e.stderr.decode("UTF-8")


class PDFlatexNotFoundError(Exception):
    pass
