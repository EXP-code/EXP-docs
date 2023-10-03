
.. _topics-index:

.. image:: exp_logo.png
   :width: 60px
   :height: 55px
   :scale: 120 %
   :alt: EXP logo
   :align: left

===========================
EXP |version| documentation
===========================

EXP is a fast high-level C++ library with Python bindings for
performing and analyzing n-body simulations using biorthogonal and
orthogonal expansions, also known as *basis function expansions (BFE)*.
The library also supports time series analysis of expansion coefficients
using multivariate Singular Spectrum Analysis (mSSA) to discover new
dynamical correlations, separate signal from noise, and visualize these
in two- and three-dimensional renderings.

There are two *entry points* into EXP:

1. The N-body code itself and Unix-style auxiliary utilities for
   manipulating and analyzing N-body phase space.
2. The Python interface to basis  C++ libraries used by the N-body
   code.  These are designed to enable your post-processing analyses
   on both EXP and other N-body simulation snapshots (Gadget, Gizmo,
   Arepo, etc.) within the Python/Jupyter ecosystem. The Python interface
   is the primary method for time series analyses.

In this documentation, **EXP** refers to the entire code base and
**pyEXP** refers to the Python EXP API.  Many users may only be
interested in pyEXP.  Since the basis function expansion concepts and
mathematics are the shared between EXP and pyEXP, we will describe
both together in this documentation.

.. _quick-start:

First steps
===========

.. toctree::
   :caption: First steps
   :hidden:

   intro/overview
   intro/install
   intro/tutorial

.. note:: TL;DR: A read through the following three topics will get you started.

:doc:`intro/overview`
    Understand what EXP is and how it can help you.

:doc:`intro/install`
    Get EXP installed on your computer.

:doc:`intro/tutorial`
    A quick-start guide to pyEXP and EXP

.. _getting-help:

Getting help
============

Having trouble? We'd like to help!

* Try the :doc:`FAQ <faq>` -- it's got answers to some common questions.
* Looking for specific information? Try the :ref:`genindex`.
* Report bugs in EXP in our `issue tracker`_.

.. _issue tracker: https://github.com/orgs/EXP-code/repositories/issues


.. note:: If you want to become an **EXPert**, please read on ...

.. _section-basics:

EXP concepts
============

.. toctree::
   :caption: EXP concepts
   :hidden:

   topics/bfetheory
   topics/codeintro
   topics/timesseries
   topics/multistep
   topics/yamlconfig

These topics provide some background detail on the software and
mathematics used in EXP.

:doc:`topics/codeintro`
    Learn about the EXP software design strategy

:doc:`topics/bfetheory`
    Learn about the mathematical principles behind BFE and EXP

:doc:`topics/timesseries`
    Descriptions for methods to analyze BFE time series

:doc:`topics/multistep`
    A quick review of EXP's ODE solver and multi time step ladder

:doc:`topics/yamlconfig`
    An example YAML configuration file for EXP


Frequently Asked Questions
==========================

.. toctree::
   :caption: Frequently Asked Questions (FAQ)
      
   faq

:doc:`faq`
    Get answers to most frequently asked questions.


How to solve specific problems
==============================

.. toctree::
   :caption: How to solve specific problems
   :hidden:

   topics/visualizing-bases
   topics/making-coefficients
   topics/saving-coefficients
   topics/visualizing-fields
   topics/make-movies
   topics/using-mssa
   topics/orbits
   topics/replay
   topics/exp-phase-space
   topics/EXP-output
   topics/debug

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

:doc:`topics/EXP-output`
    A description of the EXP N-body output generator

:doc:`topics/debug`
    Learn how to debug common problems in EXP/pyEXP

.. _extending-exp:

Extending EXP
=============

.. _extending:

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


More about EXP
==============

.. toctree::
   :caption: More about EXP
   :hidden:

   news
   contributing
   doxygen
   versioning

:doc:`news`
    See what has changed in recent EXP versions.

:doc:`contributing`
    Learn how to contribute to the EXP project.

:doc:`doxygen`
    Doxygen manual for EXP and pyEXP classes.

:doc:`versioning`
    Understand EXP versioning and API stability.
