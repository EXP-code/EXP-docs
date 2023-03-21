.. _visualizing-bases:

How to visualize the BFE bases used to make your coefficients
=============================================================

This is easy with pyEXP.  Each of the three main basis types supported
by pyEXP, ``SphericalSL``, ``Cylindrical``, and ``FlatDisk`` provides
a ``getBasis`` member function that returns the basis functions in
their native geometry.

Let's work a few simple examples to give you all you need to look at
your bases.


A spherical basis
-----------------

Start with a simple configuration file for spherical basis and
instantiate the basis:

.. code-block:: python

   # Make the halo basis config
   halo_config="""
   ---
   id: sphereSL
   parameters :
     numr:  2000
     rmin:  0.0001
     rmax:  1.95
     Lmax:  4
     nmax:  10
     scale: 0.0667
     modelname: SLGridSph.model
   ...
   """
   #
   halo_basis = pyEXP.basis.Basis.factory(halo_config)


The ``getBasis`` member for each basis returns a vectors of arrays for
the basis functions on the grid you have defined.  For the spherical
or flat disk case, the basis functions are one-dimensional functions.
We provide a beginning and ending radius in logarithmic units along
with a grid size:

.. code-block:: python

   # Get the basis grid
   #
   lrmin = -3.0
   lrmax = 0.5
   rnum  = 200
   halo_grid = halo_basis.getBasis(lrmin, lrmax, rnum)

   Now that we have the basis function grids, we can plot them.  For example:

.. code-block:: python

   # Make a logarithmically space grid in radius
   #
   r = np.linspace(lrmin, lrmax, rnum)
   r = np.power(10.0, r)

   for l in range(3):
      for n in range(5):
         plt.semilogx(r, halo_grid[l][n], '-', label="n={}".format(n))
      plt.xlabel('r')
      plt.ylabel('potential')
      plt.title('l={}'.format(l))
      plt.legend()
      plt.show()
  

Cylindrical basis
-----------------

Now let's do the same for a cylindrical basis.  The main difference
here is that the basis functions are two-dimensional merional planes.

As before let's begin by configuring and instantiating our basis:

.. code-block:: python

   # Make the disk basis config
   #
   disk_config = """
   ---
   id: cylinder
   parameters:
     acyl: 0.01
     hcyl: 0.001
     lmax: 32
     mmax: 6
     nmax: 32
     ncylorder: 8
     ncylnx: 256
     ncylny: 128
     rnum: 200
     pnum: 0
     tnum: 80
     ashift: 0.5
     vflag: 0
     logr: false
     density: false
     eof_file: .eof.cache.run0
   ...
   """

We provide a beginning and ending cylindrical radius and a beginning
and ending vertical extent, this time in linear units:

.. code-block:: python

   # Get the two-dimensional basis grid
   #
   Rmin = 0.0
   Rmax = 0.1
   Rnum = 100
   Zmin = -0.03
   Zmax =  0.03
   Znum = 40

   disk_grid = disk_basis.getBasis(Rmin, Rmax, Rnum, Zmin, Zmax, Znum)


We'll use `contourf` to visualize the meridional-plane basis functions:

.. code-block:: python

   R = np.linspace(Rmin, Rmax, Rnum)
   Z = np.linspace(Zmin, Zmax, Znum)
   #
   xv, yv = np.meshgrid(R, Z)
   #
   for m in range(3):
      for n in range(5):
         # Tranpose for contourf
         cx = plt.contourf(xv, yv, disk_grid[m][n].transpose())
         plt.xlabel('R')
         plt.ylabel('Z')
         plt.title('m, n={}, {}'.format(m, n))
         plt.colorbar(cx)
         plt.show()
  
      
