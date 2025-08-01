import numpy as np


def get_extremes_safely(values):
    values = np.asarray(values)
    finite = np.isfinite(values)
    lower = np.min(values[finite])
    upper = np.max(values[finite])
    return lower, upper


def format_options(**options) -> str:
    opts = []
    for name, value in options.items():
        if isinstance(value, bool):
            if value:
                opts.append(str(name))
        else:
            opts.append(f"{name}={value}")

    if opts:
        options_str = ",\n".join(opts)
        return f"[{options_str}]"
    return ""


def wrap_env(envname: str, wrapped: str, **options) -> str:
    return f"\\begin{{{envname}}}{format_options(**options)}\n{wrapped}\n\\end{{{envname}}}"


def format_list(items):
    return ", ".join([str(item) for item in items])
