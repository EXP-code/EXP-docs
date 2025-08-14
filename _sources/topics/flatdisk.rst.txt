.. _flatdisk_config:

How to configure a razor-thin disk
==================================

.. index:: YAML

This stanza defines the phase-space components with associated
parameters and force methods as a list.  Each list element starts with
'-' and has four fields:

==========     ===========
Key word       Explanation
==========     ===========
name           the mnemonic name for the component
parameters     a list of key: value pairs
bodyfile       the name of the ascii phase-space file to initialize this component
force          the method for computing the potential and acceleration
==========     ===========

  
The mnemonic name may contain spaces.  The body file is in EXP native
formation.  EXP has its own hierarchical phase space structure that we
call :ref:`PSP <exp-phase-space>`.  EXP provides a number of
standalone routines to manipulate, visualize and summarize the content
of PSP files.  EXP uses the list index internally to describe the
component. However, there is support for reflection by mnemonic name.

A complete example
------------------

``FlatDisk`` uses the empirical orthogonal function method (EOF)
described in :ref:`twodcyl` to find potential-density pairs that best
fit a target disk density.  This method also computes the potential
and force above and below the disk plane for coupling to
three-dimensional components. The desired target model is specified in
the YAML configuration in the `force` field stanza.  A typical force
configuration for a razor-thin exponential disk might be:

.. code-block:: yaml

    ---
    .
    .
    .
    force        :
      id         : flatdisk
      parameters :
        diskconf   : {name: expon, parameters: {acyl: 0.01}}
        nmaxfid    : 40
        rcylmin    : 0.0
        rcylmax    : 10.0
        numx       : 256
        numy       : 128
        scale      : 0.01
        knots      : 400
        Mmax       : 6
        nmax       : 12
        logr       : false
        self_consistent : true
    .
    .
    .		
    ...

Some explanation:

- ``id`` is a mnemonic name for the force, `flatdisk` in this case
- ``parameters`` is a list of key-value pairs that define the force
- ``diskconf`` defines the target density for basis construction.
  Here we are using an exponential disk with with a scale length,
  ``acyl`` of 0.01
- ``nmaxfid`` is the maximum Bessel function degree for the Bessel
  function Gram matrix used to construct the EOF basis
- ``rcylmin`` and ``rcylmax`` define the minimum and maximum radius,
  respectively, of the table of potential-density pairs in units where
  the disk scale is unity
- ``scale`` maps the cylindrical coordinates to the disk basis.
  Choosing this to be the same or similar to the ``acyl`` parameter is
  a good choice in this calse
- ``numx`` and ``numy`` are the number of grid points in the x and z
  directions, respectively, for the tabulation of the potential and
  force functions in the meridional plane
- ``knots`` is the number of quadrature knots used to compute the
  inner products in the Gram matrix
- ``Mmax`` and ``nmax`` are the maximum azimuthal degree and radial
  order, respectively, for the new basis functions
- ``logr`` is a boolean that indicates whether the radial grid is
  linear or logarithmic
- ``self_consistent`` is a boolean that indicates whether the
  force field is computed from the particle distribution at every time
  step or fixed to the initial distribution

Please note that many of these parameters have sensible defaults and
can be left out of the configuration.  They are included here as an
example.  By default, `FlatDisk` uses Bessel functions to construct
the full three-dimensional fields from the flat-disk density using the
Hankel transform (see :ref:`twodcyl`).  This method is very accurate
when the initial basis set itself are proportional to Bessel functions
and that is the default.  However, the initial basis may use the
Clutton-Brock two-dimensional basis set, optionally.  This is
experimental and requires recompiling the code.  Ask for help if you
want to consider this.


Target densities and their parameters
-------------------------------------

Exponential disk
~~~~~~~~~~~~~~~~

Name: ``expon``

Parameters:

==========     ===========
Key word       Explanation
==========     ===========
acyl           scale length
==========     ===========

Kuzmin disk
~~~~~~~~~~~

Name: ``kuzmin``

Parameters:

==========     ===========
Key word       Explanation
==========     ===========
acyl           scale length
==========     ===========

Mestel disk
~~~~~~~~~~~

Name: ``mestel``

Parameters:

==========     ===========
Key word       Explanation
==========     ===========
vrot           rotation speed
==========     ===========


Zang disk
~~~~~~~~~

Also known as the doubly tapered Mestel disk

Name: ``zang``

Parameters:

==========     ===========
Key word       Explanation
==========     ===========
vrot           rotation speed
Ninner         inner taper exponent
Mouter         outer taper exponent
Ri             inner taper radius
Ro             outer taper radius
==========     ===========

