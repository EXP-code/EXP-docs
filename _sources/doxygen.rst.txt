.. _doxygen:

====================
Index to C++ classes
====================

.. index:: Doxygen

Doxygen generates an HTML reference manual from stylized comments
written into the EXP class definitions.  This allows us to visualize
the relationships between the various classes by providing dependency
graphs, inheritance diagrams, and collaboration diagrams, which are
all generated automatically.

In short, Doxygen is a *development* resource while this ReadTheDocs
manual is a *user* resource.  For this reason, Doxygen is optional and
not built by default.  You may opt-in to the Doxygen build when
compiling EXP using the ``BUILD_DOCS`` feature (:ref:`installing EXP
<compile-features>`).  The resulting HTML directory is in
``source_dir/doc/html``.  Please see the `Doxygen web site
<https://www.doxygen.nl>` to learn more.

A brief summary of the automatically-generated documentation is
provide in the links below.

All classes, members, and utilities
===================================

* :ref:`genindex`
     
Code reference with inheritance diagrams
========================================

.. doxygenindex::
   :allow-dot-graphs:

