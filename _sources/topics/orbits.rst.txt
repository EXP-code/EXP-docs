.. _orbits:

Generating orbits in your BFE potential fields
==============================================

This is a pyEXP topic.  For doing this with EXP directly, please see 
:ref:`replaying a simulation using EXP <replay>`.

The ``pyEXP.basis.Basis`` classes allow direct evaluation of
potential, density and force fields at any position represented by the
basis and for any time represented in the coefficient time series.  I
will assume that you have already generated bases for your galaxy
components and computed coefficients.  The steps to compute some
orbits are:

1. First recreate the bases needed to represent your simulation.
   Here, we will assume a two-component galaxy described by
   ``disk_config`` and ``halo_config``.  Begin by creating the basis
   instances in pyEXP:

   .. code-block:: python

      disk_basis = pyEXP.basis.Basis.factory(disk_config)
      halo_basis = pyEXP.basis.Basis.factory(halo_config)

2. Read in the coefficient sets that you generated previously.  For example:

   .. code-block:: python

      cfiles = {'star': 'outcoef.star.run0.h5', 'dark': 'outcoef.dark.run0.h5'}
      bases  = {'star': disk_basis, 'dark': halo_basis}
      coefs  = {}
      for v in cfiles:
	coefs[v] = pyEXP.coefs.Coefs.factory(cfiles[v])


3. Finally, make some test phase space points whose orbits you wish to
   view/plot: 

   .. code-block:: python

      ps = [ 
		   [                    0.0685662,        -0.0552021,        0.00293448,           1.06493,           1.22177,         0.0375602],
		   [                     0.0270837,       -0.00199308,       -0.00424478,          0.132617,           1.03457,         -0.228147],
		   [                     0.0244691,       -0.00391702,        0.00533045,          0.524929,          0.914731,        -0.0222018],
		   [                    0.00469114,         0.0195154,        0.00621128,          -1.20355,           0.13997,           -0.1373],
		   [                    -0.0316536,        -0.0930633,         0.0153156,           1.00968,         -0.607879,          0.108066],
		   [                    -0.0672474,        -0.0226534,        0.00213119,          0.543532,          -1.50594,           -0.2269],
		   [                    0.00911594,         0.0670482,       -0.00389638,          -1.59342,         -0.156485,          0.179025],
		   [                   -0.00756623,        -0.0420422,        -0.0145696,           1.23482,         -0.367024,         -0.408862],
		   [                     0.0695395,        -0.0200928,       -0.00845714,          0.111269,           1.53921,         -0.416499]
      ]

   This particular example is taken from the ``test_orbit_better.ipynb``
   Jupyter notebook.

4. We are almost there.  The ``pyEXP.basis`` module provides two force
   routines for your convenience.  The first, ``AllTimesAccel()``
   interpolates on the Coefs data base and installs the interpolated
   coefficients for the current time in the basis instance.  The
   ``SingleTimeFunc`` interpolates on the Coefs data base for a single
   fixed time and sets the interpolated coefficients once at the
   beginning of the integration.  This implements a fixed potential
   model.  Finally, we call the ``IntegrateOrbits`` class to generate
   the orbits as follows:

   .. code-block:: python

      model = [[bases['star'], coefs['star']], [bases['dark'], coefs['dark']]]
      func = AllTimesAccel()
      times, orbits = pyEXP.basis.IntegrateOrbits(0.0, 0.5, 0.01, ps, model, func)

   ``times`` is a one-dimension array of time evaluations and
   ``orbits`` is a three-dimensional array whose first index is the
   orbit count, the second is x, y, z, u, v, w indexed from 0,...,5
   and the third is the time index.  So orbits may be plotted in
   coordinates or time, e.g. using pyplot, however you see fit.


If you'd like to write your own force function, the ``AccelFunc`` base
class can be inherited by a native Python class and the ``evalcoefs``
may be implemented in Python and passed to ``IntegrateOrbits`` in the
same way as a native C++ class.
