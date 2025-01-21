Pykz, Tikz generation from Python
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:
   
   api
   gallery/index

Generate beautiful, publication-ready figures with the power of Tikz and 
pgfplots, with a comfortable, familiar Python syntax.

``pykz`` aims to provide a syntax similar to `matplotlib <https://matplotlib.org/>`_, 
but with the possibility of directly outputting (and controlling!)
your tikz code.

The benefit over alternatives like
`tikzplotlib <https://github.com/nschloe/tikzplotlib>`_ is ``pykz`` 
was designed explicitly with pgfplots in mind, whereas the goal of tikzplotlib
is to map matplotlib concepts to pgfplots. This is arguably more convenient 
if you already have code for matplotlib, but it often still requires manual
tweaking to the resulting tex-files. ``pykz`` aims to provide more 
control over the final output directly in Python, so no manual 
tweaking is required afterwards.

Installation
-------------
To install pykz, run:

.. code-block:: console

   $ pip install pykz

Quick Start
------------

``pykz`` provides a simple high-level interface for common plotting operations.
For instance, see :doc:`gallery/basic_inline`

For more examples, see the :doc:`gallery/index`

Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
