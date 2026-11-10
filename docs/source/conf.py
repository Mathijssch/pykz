# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
project = 'pykz'
copyright = '2025, Mathijs Schuurmans'
author = 'Mathijs Schuurmans'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser',
    'sphinx_gallery.gen_gallery',
    "sphinx_codeautolink",
]

templates_path = ['_templates']
exclude_patterns = []


# The reset hook snapshots existing PDFs before executing each example.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gallery_scraper import PDFScraper

pdf_scraper = PDFScraper()


sphinx_gallery_conf = {
    'examples_dirs': '../../examples',   # Path from conf.py to examples folder
    'recommender': {"enable": True, "n_examples": 5, "min_df": 3, "max_df": 0.9},
    'gallery_dirs': 'gallery',     # This will be created relative to doc build
    'filename_pattern': '/',
    'image_scrapers': (pdf_scraper),  # Add PDF scraper
    'reset_modules': ('matplotlib', 'seaborn', pdf_scraper.reset),
    'reset_modules_order': 'before',
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
