<div align="center">
    <h1>Pykz</h1>
    A Python library to generate tikz code.
</div> 

## Disclaimer 

This library is in very early development. Use at your own risk.

## Examples

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
![sample output](images/test-basic-plot_hidpi.png)

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
![sample output](images/circles_hidpi.png)


## TO-DO 

- [ ] When a color is passed to a point, also pass it to the label options.
- [ ] Complete the README
- [ ] More examples
- [ ] More functionality

