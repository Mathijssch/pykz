"""
Histograms
=========================
Generating histograms directly from data.
"""

# %%
# This examples demonstrates some basic methods for plotting histograms using Pykz.

# %%
# We import the usual libraries.
import numpy as np
import pykz

# %%
# Let's generate some data. We do this in exactly the same way as you would using
# Matplotlib.

dataset = [1, 4, 5, 3, 3, 5, 3, 2, 5, 7, 8, 5]

# %%
# By default, `pykz` will automatically determine the number of bins.

hist = pykz.hist(dataset)
pykz.xlabel("Values")
pykz.ylabel("Frequency")

# Export your tex code as a standalone file
pykz.save("histogram.tex", standalone=True)
# Build the pdf
pykz.io.export_pdf_from_file("histogram.tex")


# %%
# We can also determine the number of bins manually

ax = pykz.gca().remove(hist)
hist = pykz.hist(dataset, bins=5)

# Export your tex code as a standalone file
pykz.save("histogram_manual.tex", standalone=True)
# Build the pdf
pykz.io.export_pdf_from_file("histogram_manual.tex")
