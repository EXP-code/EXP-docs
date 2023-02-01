
===================================
EXP documentation quick start guide
===================================

This file provides a quick guide on how to compile the EXP documentation.


Setup the environment
---------------------

To compile the documentation you need Sphinx Python library. To
install it along with the ReadTheDocs theme, run the following commands:

::

   pip install sphinx
   pip install sphinx-rtd-theme

For a Linux system with `apt` (e.g. Ubuntu), you can do:

::

   apt-get install python3-sphinx python3-sphinx-rtd-theme


Compile the documentation
-------------------------

To compile the documentation (to classic HTML output) run the
following command from this directory::

    make html

Documentation will be generated (in HTML format) inside the
``_build/html`` directory.

Other formats are available.  For example, you can make epub format
with::

  make epub

I've tested this with a standard epub reader under Linux and it 
works, but does not correctly render the LaTeX.  You can generate a
PDF file using::

  make latexpdf
  
There are a few LaTeX mistakes but it *mostly* works.  These errors
are probably easily fixed.  Type 'q' to get a mostly usable PDF file.

View the documentation
----------------------

To view the documentation run the following command point your browser
at `_build/html/index.html`


Start over
----------

To clean up all generated documentation files and start from scratch run::

    make clean

Keep in mind that this command won't touch any documentation source files.


