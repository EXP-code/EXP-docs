.. _faq:

Frequently Asked Questions
==========================

.. _faq-EXP-bs-cmp:

I only want pyEXP, do I need C++ to compile EXP?
------------------------------------------------

Yes, EXP is an C++ library with Python support provided by
`pybind11`_.  So, you need to compile the C++ library first.  However,
you can compile pyEXP without the N-body code itself.  Please see
:ref:`the Installation Guide <intro-install>` for compilation and
configuration details.

.. _pybind11: https://pybind11.readthedocs.io/

Why would I use EXP rather than pyEXP?
--------------------------------------

The EXP N-body code is designed to accurately model disequilbria from
modest satellite interactions, the gravitational coupling between
different galaxy components, and model internal instabilities.  The
bases used in EXP are also suitable for Hamiltonian perturbation
theory calculations.  This provides a self-consistency check and path
to understanding the non-linear development of linear predictions.
The EXP N-body code *will not* work well for major mergers!

pyEXP uses the same library routines as EXP but applies to analyses of
existing simulations done with EXP or most well-known cosmological
N-body codes.  The EXP code base provides stand-alone Unix routines
for these analyses, too.  If you want to analyze existing N-body
simulation output and prefer the Jupyter/Python ecosystem, pyEXP is
what you want.
