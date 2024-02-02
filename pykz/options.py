from .formatting import format_options
from collections.abc import Mapping


class Options(Mapping):

    def __init__(self, **options):
        self._opt_dict = {key.replace("_", " "): value
                          for (key, value) in options.items()
                          if value is not None}

    def format(self) -> str:
        return format_options(**self._opt_dict)

    def set_option(self, name: str, value: str):
        self._opt_dict[name.replace("_", " ")] = value

    def set_options(self, **options):
        for k, v in options.items():
            self.set_option(k, v)

    # Dict-like methods

    def __getitem__(self, key):
        return self._opt_dict[key]

    def __setitem__(self, key, value):
        self._opt_dict[key] = value

    def __delitem__(self, key):
        del self._opt_dict[key]

    def __iter__(self):
        return iter(self._opt_dict)

    def __len__(self):
        return len(self._opt_dict)

    def __dict__(self):
        return self._opt_dict