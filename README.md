<div align="center">
    <h1>Pykz</h1>
    <b>A Python library to generate tikz code</b><br><br>
<img alt="Static Badge" src="https://img.shields.io/badge/docs-examples-green?style=flat-square&link=https%3A%2F%2Fmathijssch.github.io%2Fpykz%2Fgallery%2Findex.html">
<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/pykz?style=flat-square&logo=pypi&color=green&link=https%3A%2F%2Fpypi.org%2Fproject%2Fpykz">
<img alt="GitHub License" src="https://img.shields.io/github/license/mathijssch/pykz?style=flat-square&color=green">
<br><br>
</div> 

Generate beautiful, publication-ready figures with the power of Tikz and pgfplots,
with a comfortable, familiar Python syntax.

pykz aims to provide a syntax similar to matplotlib,
but with the possibility of directly generating (and controlling!) your tikz code.

The benefit over alternatives like [tikzplotlib](https://github.com/nschloe/tikzplotlib) is pykz was designed explicitly with pgfplots in mind,
whereas the goal of tikzplotlib is to map matplotlib concepts to pgfplots.
This is arguably more convenient if you already have code for matplotlib,
but it often still requires manual tweaking to the resulting tex-files.
pykz aims to provide more control over the final output directly in Python,
so no manual tweaking is required afterwards.

## Usage

### Basic plotting

Pykz has a simple, matplotlib-like interface for basic plotting.
```

import numpy as np
import pykz

x = np.linspace(0, 10, 100)
y = np.sin(x)

pykz.plot(x, y)

# (Optional) save the tikz code to a file.
pykz.save("test-basic-plot.tex")

# Save the Tikz code to a temporary file, compile it, and open the pdf in the default viewer.
pykz.preview()
```
<div align="center">
<img src="https://mathijssch.github.io/pykz/_images/sphx_glr_basic_inline_001.png" alt="Sample output" width="60%">
</div>

### Using Tikz primitives 

Alternatively, you can use standard TikZ 
drawing primitives, without using pfgplots.
Options passed to the TikZ command are passed as keyword arguments.
```
import pykz


rect = pykz.rectangle((-1, -1), (1, 1))
circle = pykz.circle((2, 0), (1), fill="red")

rect2 = pykz.rectangle((1, 1), (2, 3), fill="cyan")

# Dump the generated tikz code to the stdout.
print(pykz.dumps())


# Save the Tikz code to a temporary file, compile it, and open the pdf in the default viewer.
pykz.preview()
```
out: 
```
\documentclass[tikz]{standalone}

\begin{document}
\begin{tikzpicture}
\draw(-1.000000000, -1.000000000) rectangle (1.000000000, 1.000000000);
\draw[fill=red](2.000000000, 0.000000000) circle (1);
\draw[fill=cyan](1.000000000, 1.000000000) rectangle (2.000000000, 3.000000000);

\end{tikzpicture}
\end{document}
```
<div align="center">
<img src="https://mathijssch.github.io/pykz/_images/sphx_glr_circles_and_squares_001.png" alt="Sample output" width="60%">
</div>
For more examples, visit the [online documentation]()
