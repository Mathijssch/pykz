"""
Bar plots
=========================
Generating histograms directly from data.
"""

# %%
# This examples demonstrates some basic methods for creating bar plots

import pykz

# %%
# Let's generate some data. We do this in exactly the same way as you would using
# Matplotlib.

labels = [1, 2, 3]
values = [1, 4, 5]

# %%
# By default, `pykz` will automatically determine the number of bins.

hist = pykz.bar(labels, values)
pykz.xlabel("Values")
pykz.ylabel("Frequency")

# Export your tex code as a standalone file
pykz.save("bar.tex", standalone=True)
# Build the pdf
pykz.io.export_pdf_from_file("bar.tex")
