.. _intro-pyEXP-tutorial:

==============
pyEXP Tutorial
==============

.. index:: sort: pyEXP; tutorial

In this tutorial, we'll assume that EXP is already installed on your system.
If that's not the case, see :ref:`intro-install`.

Making BFE coefficients from phase-space data
---------------------------------------------

In this first example, we will assume that you have an ascii file of
particles from a simulation of halo.  We'll assume that this file is
called `my.dark halo` where each line in the file is the mass,
x-position, y-position, z-position, etc. for each particle.  We also
assume that we have a profile, `SLGridSph.model`, describing our halo
consisting of 4 columns: the radius, the density, the enclosed mass,
and the gravitational potential.  There is a header line that
describes the number of radii (profile lines) in the file.

We begin by importing some Python modules:

.. code-block:: python

   import os
   import pyEXP
   import numpy as np

   os.chdir('/path/to/my/data')

The last line is optional if you are already in the directory that
contains the working files `my.dark halo` and `SLGridSph.model`.

We then use pyEXP to construct and :index:`adaptive basis` matching
the profile in the file as follows:

.. code-block:: python

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

   # Construct the basis instances
   #
   basis = pyEXP.basis.Basis.factory(config)

The string `config` is the :index:`YAML` file needed by pyEXP to
specify the basis.  In this case, the adaptive spherical basis is the
`sphereSL` type.  The parameters `rmin` and `rmax` define the inner
and outer radii for the basis, `Lmax` and `nmax` describe the maximum
harmonic and radial orders for the basis, respectively.  The `scale`
parameter adjusts the internal coordinate mapping and a good choice is
the characteristic radius of the halo.

We now read our phase space data:

.. code-block:: python

   # Open the file and read the array.
   #
   bodyfile = 'my.dark halo'
   if not os.path.exists(bodyfile):
      print("You need to use psp2ascii to make an ascii input file, e.g.\n"
            "'psp2ascii -f OUT.run0.00010'")
      exit(1)

   data = np.loadtxt(bodyfile, skiprows=1, usecols=(1, 2, 3, 4))
   print(data.shape)

   # Call the basis to generate coefficients
   #
   coef = basis.createFromArray(data[:,0], data[:,1:4], time=3.0)

The work horse in the block above is the member function
`createFromArray()` which takes an N x 1 array of masses and a N x 3 array
of positions as input.  We may specify the time of this snapshot using
the `time` option.

The `coef` variable is a structure that contains all of the
coefficient data for the phase space.  We then add that structure to a
database of class, called `Coefs`, which maintains a dictionary of
`coef` instances for every snapshot of interest.  The example here
only adds the single coefficient structure for `time=3.0`.  A
production pipeline would do this for every snapshot.

One we have added all of our `coef` instances to the `Coefs` database,
we write the result into an HDF5 file.  This file can be saved and
reread for any number of subsequent analyses.

Putting all of this together, we have the following code:

.. code-block:: python

   # Print the data for a check
   #
   print("Time=", coef.time, " geometry=", coef.geometry)
   print("Shape=", coef.data.shape)
   print("Data=\n", coef.data)

   # Make an HDF5 file
   #
   coefs = pyEXP.coefs.Coefs.makecoefs(coef)
   coefs.add(coef)
   coefs.WriteH5Coefs("table_to_coefs");
   print("Wrote coefficients")

   print("Times are:")
   print(coefs.Times())
   print(coefs.getCoefStruct(3.0))

   time = 3.0
   print("Setting to T=", time)
   basis.set_coefs(coefs.getCoefStruct(time))



Next steps
==========

This tutorial covered only the basics of pyEXP, but there's a lot of other
features not mentioned here. 
