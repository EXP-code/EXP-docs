# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EXP'
copyright = '2023-2025, EXP-code collaboration'
author = 'EXP-code collaboration'
release = '0.16'
version = '7.x'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.graphviz',
    'breathe',
    'sphinx_copybutton',
    'nbsphinx',
    'nbsphinx_link'
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.rst']

breathe_projects = {"EXP": "doxyxml/"}
breathe_default_project = "EXP"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_logo = 'exp_logo_white.png'
html_static_path = ['_static']

# -- Turn on figure numering -------------------------------------------------
numfig = True

# -- Extension configuration -------------------------------------------------
nbsphinx_execute = 'never'

# -- Grab files from pyEXP-examples -----------------------------------------
import os

os.system("cd intro/notebook; rm *ipynb*; wget -L https://raw.githubusercontent.com/EXP-code/pyEXP-examples/refs/heads/main/Tutorials/Introduction/Part1-Coefficients.ipynb; wget -L https://raw.githubusercontent.com/EXP-code/pyEXP-examples/refs/heads/main/Tutorials/Introduction/Part2-Analysis.ipynb")

