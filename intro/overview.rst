.. _intro-overview:

===============
EXP at a glance
===============

EXP is a library that implements both N-body simulations and analysis
of simulations.  The code uses object-oriented design patterns to
exploit the similarity in overall structure of all :ref:`biorthogonal
expansions <bfetheory>` for ease of implementation and maintenance.
The class hierarchy enables reuse and reconfiguration for any number
of phase-space components whose gravity may be represented by a
appropriate biorthgonal bases and direct gravity methods.  The
object-oriented design enforces minimal consistency while retaining
flexibility.  This hierarchy is reflected in the latest addition to
EXP: a set of Python bindings, **pyEXP**, that enable analyses of
simulations in the Python/Jupyter ecosystem.

EXP, the N-body code
====================

EXP n-body users may write, compile and contribute new phase space
operators for applying perturbations, new force methods, etc. without
changing or recompiling the base code. See :ref:`modules
<usermodules>` for details and a simple example.  **pyEXP** brings the
power of BFE and mSSA for discovering dynamical features and
mechanisms from N-body snapshots generally and allows you to combine
them with your existing Python workflow.

pyEXP, for N-body discovery
===========================

.. index:: pyEXP

All of the main analysis features of EXP are available as a Python
module, enabled by pybind11 (https://pybind11.readthedocs.io/).  This
API provides nearly all of the EXP functionality to the Python user
except for running n-body simulations.


Both variants of the code, the C++ n-body system and the pyEXP
analysis system, have github repositories, `EXP-examples`_ and
`pyEXP-examples`_, than provide detailed tutorials and examples.

.. _EXP-examples: https://github.com/orgs/EXP-examples
.. _pyEXP-examples: https://github.com/orgs/pyEXP-examples


A simple pyEXP illustration
===========================

.. index:: pair: pyEXP; simple example

We anticipate that most users will be interested in using pyEXP in
their N-body analysis workflow.  In order to show you what pyEXP
brings to the table, we'll walk you through an example of a simulation
analysis.

Here's the code for computing coefficients::

     import os
     import pyEXP
     import numpy as np
     import matplotlib.pyplot as plt

     # Make the halo basis config
     config="""
     ---
     id: sphereSL
     parameters :
       numr: 2000
       rmin: 0.0001
       rmax: 1.95
       Lmax: 4
       nmax: 10
       scale: 0.0667
       modelname: SLGridSph.model
     ...
     """

     # Construct the basis
     #
     basis = pyEXP.basis.Basis.factory(config)

     # Open the file and read the array.  The file is an ascii phase-space file
     # with mass, x, y, z in the first four columns with a leading  header line
     #
     bodyfile = 'bodies.dat'

     data = np.loadtxt(bodyfile, skiprows=1, usecols=(1, 2, 3, 4))

     # Call the basis to generate coefficients
     #
     coef = basis.createFromArray(data[:,0], data[:,1:4], time=3.0)

     # Make an HDF5 file
     #
     coefs = pyEXP.coefs.Coefs.makecoefs(coef)
     coefs.add(coef)
     coefs.WriteH5Coefs("table_to_coefs");
     
     # Set the basis expansion to these coefficients
     #
     time = 3.0
     basis.set_coefs(coefs.getCoefStruct(time))
   

Put this in a text file, name it to something like ``make_coefs.py``
and run the it using::

    python3 make_coefs.py


What just happened?
-------------------

The script ``make_coefs.py`` begins by defining a spherical basis to
represent your halo.  The configuration is specified by YAML schema
called ``config``.  This file defines the type of basis and parameters
needed for basis construction, including a file describing the density
and potential model for your basis.

pyEXP is then ready to make the coefficients from your phase-space
data.  This example assumes that the mass and positions of your
particles are in columns 1, 2, 3, 4 of the file.  In most cases, you
will use your standard phase-space pipeline for any necessary
reprocessing such as centering and other coordinate transformations.

The coefficients are then computed by the newly made basis from this
data in the ``basis.createFromArray()`` call.  The coefficients are
then written to an HDF5 file safe keeping and installed in the
``basis``.   The ``basis`` can be evaluated to provide visualizations
of the field values implied by these coefficients.

.. note::

   The class ``Basis`` class interacts with a ``ParticleReader`` class
   that can read most standard HDF5-type phase-space and Tipsy files
   directly without have to make a data table.

.. _topics-whatelse:

What else?
==========

You've seen a simple example of using pyEXP to make coefficients from
phase-space data using an adaptive basis made from a halo model of
your choice.  This is just the surface. EXp and pyEXP provide many
powerful features for learning about the dynamical details of your
simulations, including:

* Built-in support for reading most simulation data from their native
  phase-space files including files that have been 'split' by parallel
  writing.

* EXP and pyEXP allow for any number of bases and any number of
  phase-space components.  For example, one can produce coefficients
  from disks, halos, bulges and even satellites or substructure
  simultaneously.

* Support for writing and installing Python call backs for computing
  custom ancillary field data or summary statistics from phase-space
  data.

* Support for evaluating the density, potential and force fields for
  visualization using matplotlib and in file format (ascii or VTK)
  external readers.

* Support for orbiting particles in the force fields implied by the
  coefficients.  You have the option of fixing the gravitational
  potential or allowing it to evolve in time.  You also have the
  choice of providing some or all of the variation present in the
  coefficient sets.

* Support for spectral analysis of the coefficients the coefficient
  time series.  Because these series from an ensemble of n-body
  snapshots represent the spatial variation of features in time, we
  can learn about the patterns in space and time together.  Spectral
  analysis is provided by a custom implementation of multivariate
  Singular Spectrum Analysis (mSSA).



What's next?
============

The next steps for you are to

1. :ref:`install EXP <intro-install>`
2. :ref:`follow through the pyEXP tutorial <intro-pyEXP-tutorial>` or the
3. :ref:`EXP tutorial <intro-EXP-tutorial>`

to learn how to create a full-blown EXP analysis or simulation and
analysis project. Thanks for your interest!

