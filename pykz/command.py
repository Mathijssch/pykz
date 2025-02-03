from __future__ import annotations

from .tikzcode import Tex
from .options import OptionsMixin


class Command(Tex, OptionsMixin):
    r"""A LaTeX Command of the form `\<cmdname>[<options>]<middle>{<arg1>}{<arg2>}...`."""

    def __init__(self, cmd: str, *arguments, **options):
        self.cmd_name: str = cmd
        # self._options: Options = Options(**options)
        self._arguments: list[Tex] = []
        for argument in arguments:
            self.add_argument(argument)
        self.init_options(**options)
        self._endline = True
        self._escape = True

    def add_argument(self, argument: str | Tex):
        if isinstance(argument, str):
            argument = Tex(argument)
        self._arguments.append(argument)

    def _format_middle(self) -> str:
        return ""

    def _format_post(self) -> str:
        return ""

    @property
    def arguments(self) -> list[Tex]:
        return self._arguments

    def _format_arguments(self) -> str:
        argument_str = ""
        for argument in self.arguments:
            argument_str += f"{{{argument.get_code()}}}"
        return argument_str

    def get_code(self) -> str:
        options_str = self.options.format()
        argument_str = self._format_arguments()
        end = ";" if self._endline else ""
        start = "\\" if self._escape else ""
        return f"{start}{self.cmd_name}{options_str}{self._format_middle()}{argument_str}{self._format_post()}{end}"
