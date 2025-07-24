# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os, sys
import subprocess

# -- Generate doxygen xml prior to build --------------------------------------

# Define the repository URL and target directory
#
repo_url  = "https://github.com/EXP-code/EXP.git"
clone_dir = "exp_repo"
branch    = "SLboundaries"
doxyfile  = "exp.cfg.breathe"
doxy_dir  = "doc"

# Cache the current working directory
#
build_dir = os.getcwd()

# Clone the EXP repository if it doesn't exist
#
if not os.path.exists(clone_dir):
    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

# Move to source and get the desired branch
#
os.chdir(clone_dir)
subprocess.run(["git", "checkout", branch])
os.chdir(doxy_dir)

# Ensure Doxygen is installed and its executable is in your PATH
#
subprocess.run(["doxygen", doxyfile], check=True)

# Build pyEXP to populate Python API documenation
#
os.chdir('..')

# Workaround for cmake version
#
subprocess.run(['cp', 'CMakeLists.txt', 'CMakeLists.txt.orig'])
command_to_pipe = subprocess.Popen(['cat', 'CMakeLists.txt.orig'], stdout=subprocess.PIPE)
foutput = open('CMakeLists.txt', 'w')
sed_command = subprocess.Popen(['sed', 's/VERSION 3.25/VERSION 3.22/'], stdin=command_to_pipe.stdout, stdout=foutput)
foutput.close()
command_to_pipe.stdout.close()

# Make build directory and begin
#
if not os.path.exists('build'):
    subprocess.run(["mkdir", "build"], check=True)
os.chdir('build')
subprocess.run(['cmake', '-DCMAKE_BUILD_TYPE=Release -DENABLE_USER=NO -DENABLE_NBODY=NO -DEigen3_DIR=$EIGEN_BASE/share/eigen3/cmake -Wno-dev', '..'])
subprocess.run(['make', '-j8'])

# Return to top level
#
os.chdir(build_dir)


# Add 'my_module_path' to the beginning of sys.path
#
my_module_path = os.path.join(build_dir, 'exp_repo/build/pyEXP')
sys.path.insert(0, my_module_path)

# Begin Sphinx configuration

# -- project information -----------------------------------------------------
#
project = 'EXP'
copyright = '2023-2025, EXP-code collaboration'
author = 'EXP-code collaboration'
release = '0.17'
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

breathe_projects = {"EXP": "exp_repo/doc/xml/"}
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
os.system("cd intro/Tutorials; rm *ipynb*; wget -L https://raw.githubusercontent.com/EXP-code/pyEXP-examples/refs/heads/main/Tutorials/Introduction/Part1-Coefficients.ipynb; wget -L https://raw.githubusercontent.com/EXP-code/pyEXP-examples/refs/heads/main/Tutorials/Introduction/Part2-Analysis.ipynb")

