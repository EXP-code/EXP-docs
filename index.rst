.. EXP documentation master file, created by sphinx-quickstart on Mon
   Dec 26 12:58:04 2022.  You can adapt this file completely to your
   liking, but it should at least contain the root `toctree`
   directive.

.. _topics-index:

===========================
EXP |version| documentation
===========================

EXP is a fast high-level C++ library with Python bindings for
performing and analyzing n-body simulations using biorthogonal and
orthogonal expansions.  The library can use expansion coefficients for
time series analysis using multivariate Singular Spectrum Analysis
(mSSA) to discover new dynamical correlations, separate signal from
noise, and visualize these in two- and three-dimensional renderings.

There are two *entry points* into EXP:

1. The N-body code itself and auxiliary utilities for manipulating and
   analyzing N-body phase space.
2. The Python interface to the same C++ libraries used by the N-body
   code.  These are designed to enable all of the post-processing
   analyses on both EXP and other N-body simulation snapshots
   (Gadget, Gizmo, Arepo, etc.).

In this documentation, EXP refers to the entire code base and pyEXP
refers to the Python EXP API.  We anticipate that many users will be
interested in *only* pyEXP.  Since the concepts and mathematics is
the same regardless, we will describe both together in this
documentation.

.. _getting-help:

Getting help
============

Having trouble? We'd like to help!

* Try the :doc:`FAQ <faq>` -- it's got answers to some common questions.
* Looking for specific information? Try the :ref:`genindex` or :ref:`modindex`.
* Report bugs in EXP in our `issue tracker`_.

.. _issue tracker: https://github.com/orgs/EXP-code/repositories/issues


First steps
===========

.. toctree::
   :caption: First steps
   :hidden:

   intro/overview
   intro/install
   intro/pyEXP-tutorial
   intro/EXP-tutorial

:doc:`intro/overview`
    Understand what EXP is and how it can help you.

:doc:`intro/install`
    Get EXP installed on your computer.

:doc:`intro/pyEXP-tutorial`
    Your first pyEXP example project.

:doc:`intro/EXP-tutorial`
    Your first EXP example project.

.. _section-basics:

EXP concepts
============

.. toctree::
   :caption: EXP concepts
   :hidden:

   topics/codeintro
   topics/bfetheory
   topics/ssa
   topics/multistep
   topics/yamlconfig

:doc:`topics/codeintro`
    Learn about the EXP software design strategy

:doc:`topics/bfetheory`
    Learn about the mathematical principles behind BFE and EXP

:doc:`topics/ssa`
    A review of Singular Spectrum Analysis and its application to BFE 

:doc:`topics/multistep`
    A quick review of EXP's multi time step ladder

:doc:`topics/yamlconfig`
    An example YAML configuration file for EXP


Solving specific problems
=========================

.. toctree::
   :caption: Solving specific problems
   :hidden:

   faq
   topics/visualizing-bases
   topics/making-coefficients
   topics/saving-coefficients
   topics/visualizing-fields
   topics/make-movies
   topics/using-mssa
   topics/orbits
   topics/exp-phase-space
   topics/debug

:doc:`faq`
    Get answers to most frequently asked questions.

:doc:`topics/visualizing-bases`
    Learn how to visualize the EXP bases using pyEXP

:doc:`topics/making-coefficients`
    Get familiar with producing coefficients for particle data in pyEXP

:doc:`topics/saving-coefficients`
    Learn how to save and read the coefficients you have produced
    from your N-body snapshots in pyEXP

:doc:`topics/visualizing-fields`
    Learn how to convert your coefficients to physical fields and
    visualize them with Python and pyEXP

:doc:`topics/make-movies`
    Make some movies from your fields in Python

:doc:`topics/using-mssa`
    Learn how to let your simulation 'speak for itself' using
    multivariate Singular Spectrum Analysis

:doc:`topics/orbits`
    Compute orbits in the gravitational potential fields implied by
    your coefficients, and why you might want to do this

:doc:`topics/exp-phase-space`
    How to use and manipulate the EXP native phase-space format

:doc:`topics/debug`
    Learn how to debug common problems in EXP/pyEXP

.. _extending-exp:

Extending EXP
=============

.. toctree::
   :caption: Extending EXP
   :hidden:

   topics/design
   topics/usermodules
   topics/newforces


:doc:`topics/design`
    Understand the EXP architecture.

:doc:`topics/usermodules`
    How to use EXP's dynamic module loader to import your own external
    force routines

:doc:`topics/newforces`
    How to write your own custom force routines


All the rest
============

.. toctree::
   :caption: All the rest
   :hidden:

   news
   contributing
   versioning

:doc:`news`
    See what has changed in recent EXP versions.

:doc:`contributing`
    Learn how to contribute to the EXP project.

:doc:`versioning`
    Understand EXP versioning and API stability.
