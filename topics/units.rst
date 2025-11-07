.. _units:

Units in EXP and pyEXP
======================

Overview
--------

The EXP N-body code assumes the gravitational constant ``G=1`` and
accepts any mass, position and velocity units consistent with that
assumption.  In other words, it does not enforce any particular unit
set.

pyEXP will also accept any mass, position, time, and velocity units
provided by the imported simulation as well as an arbitrary value of
the gravitational constant. Explicit units types and the gravitational
constant `G` may be set at construction time as we will describe below
in :ref:`unit-schema`.  pyEXP requires the user to set units
explicitly when coefficient sets are constructed. See
:ref:`intro-pyEXP-tutorial`. There is no default.

All unit information is written into the EXP coefficient files as HDF5
attributes.  Also see :ref:`hdf5-unit-attributes` for details.

.. _unit-scheme:

The EXP unit schema
-------------------

EXP requires one of the following two sequences of units:

1. Mass, Length, Time, gravitational constant (G)

2. Mass, Length, Velocity, gravitational constant (G)


Each unit is a ``tuple`` which takes the form::

  ('unit type', 'unit name', <float value>)

The type and name strings are checked against the allowed values as follows:

- The ``unit type`` is one of 'length', 'mass', 'time', 'velocity' or
  'G'. The internal parser will accept a variety of aliases for these
  such as 'Length', 'Len', 'len', 'l', 'L' for 'length'; 'Mass', 'm',
  'M' for 'mass'; 'Time', 't', 'T' for 'time', 'vel',
  'Vel', 'Velocity', 'v', 'V' for 'velocity'; and 'Grav', 'grav',
  'grav_constant', 'Grav_constant', 'gravitational_constant',
  'Gravitational_constant' for 'G'.

- The ``unit name`` is one of the usual unit names for each of the
  ``unit type``.  The allowed list is a subset of the standard
  `astropy` strings.  For example, 'pc' or 'kpc' for 'length'.  There
  is also a 'none' type which implies no assigned physical units.

- The floating value defines the number of each unit for the type.
  The value can be any valid floating-point number.

For development reference, these allowed strings are defined in
`expui/UnitValidator.cc` in the EXP source tree.

As an example, a Gadget user might define mass units as::

  ('mass', 'Msun', 1.0e10)

The full units specification is a list of tuples that includes one of
the four sequences.  In C++, the list is a ``std::vector`` of tuples.

As an example, all native EXP simulations have the following unit
lists::

 [('mass', 'none', 1.0f), ('length', 'none', 1.0f), ('time', 'none',
 1.0f), ('G', 'none', 1.0f)]
 

Units in pyEXP
--------------

The ``pyEXP.basis`` classes will use the units specified by the user
in the ``pyEXP.coefs`` class created from simulation snapshots (see
:ref:`intro-pyEXP-tutorial`) or read by the coefficient factory from
an existing HDF5 file to produce accelerations using the value of the
gravitational constant and length units provided by the user.


.. _units-interface:

The Units interface
-------------------

The `pyEXP` user interface includes two member functions for explicitly
setting and removing units as part of the `Coef` class.  For setting
units, we have:

   .. code-block:: python

      setUnits(name, unit, value)
      setUnits(list)
      removeUnits(name)

where ``name`` and ``unit`` are strings and ``value`` is a float.  The
list is a list of tuples of ``(name, unit, value)``.

The C++ UI echos the functions above and adds functions to retrieve
units

   .. code-block:: C++

      void setUnits(const std::string name, const std::string unit, float value);
      void setUnits(std::vector<std::tuple<std::string, std::string, float>> list);
      void removeUnits(const std::string name);
      std::vector<std::tuple<std::string, std::string, float>> getUnits();

and to interact with HDF files that will only be of interest to
developers creating new coefficient classes.


.. _hdf5-unit-attributes:

The HDF5 specification
----------------------

.. note:: This section assumes basic familiarity with HDF5 and `h5py`
	  in particular.

EXP HDF5 coefficient files contain a full set of metadata describing
their basis type, basis parameters, geometry, and units as attributes
of the root ("/") group.  The ``snapshots`` group contains all of the
coefficient data and metadata (such as center and rotation
information) for each snapshot time in the coefficient set.

The units information is stored in the root group as dataset named
"Units".  The dataset is a sequence  or list of 4 tuples.  Each tuple
has three fields: two fixed length strings of sixteen (16) characters
and a float value.

For an EXP run, the units specification appears as dataset in the root
group with the following hierarchy::

     DATASET "Units" {
      DATATYPE  H5T_COMPOUND {
         H5T_STRING {
            STRSIZE 16;
            STRPAD H5T_STR_NULLTERM;
            CSET H5T_CSET_UTF8;
            CTYPE H5T_C_S1;
         } "name";
         H5T_STRING {
            STRSIZE 16;
            STRPAD H5T_STR_NULLTERM;
            CSET H5T_CSET_UTF8;
            CTYPE H5T_C_S1;
         } "unit";
         H5T_IEEE_F32LE "value";
      }
      DATASPACE  SIMPLE { ( 4 ) / ( 4 ) }
      DATA {
      (0): {
            "G",
            "none",
            1
         },
      (1): {
            "length",
            "none",
            1
         },
      (2): {
            "mass",
            "none",
            1
         },
      (3): {
            "time",
            "none",
            1
         }
      }
   }
  

A units attribute list could be easily added to existing HDF5 files
using `h5py` using the schema described above.  For example, assuming
that you already have an open HDF5 coefficient file named `f`, the
units described in the scheme above could be added to `f` with the
following code:

   .. code-block:: python

      import h5py
      import numpy as np

      # Define the compound datatype with fixed-length ASCII strings and a float32
      dt = np.dtype([
		   ('name', 'S16'),   # Fixed-length ASCII string of 16 bytes
		   ('unit', 'S16'),   # Fixed-length ASCII string of 16 bytes
		   ('value', '<f4')   # Little-endian 32-bit float
		   ])

      # Create the dataset data as a numpy array
      data = np.array([
          (b'G',       b'none', 1.0),
	  (b'length',  b'none', 1.0),
	  (b'mass',    b'none', 1.0),
	  (b'time',    b'none', 1.0),
	  ], dtype=dt)

      # Open the HDF5 coefficient file and add the dataset
      with h5py.File('outcoef.disk.runtag', 'a') as f:
          # 'a' mode opens file for read/write, creates if not exist

	  # Create dataset 'Units'
	  if 'Units' in f:
              # Optional: remove existing dataset if you want to overwrite
              del f['Units']  
	  dset = f.create_dataset('Units', data=data, dtype=dt)

      # File is automatically closed on leaving the 'with' block, flush and
      # update saved data on disk
