.. _EXP-output:

How the EXP N-body code selects what and when to write data
===========================================================

Output modules
--------------

The `OutputContainer` class contains a list of instances of
classes that gather information about the running simulation as
described in :ref:`the code intro <code-intro>`.  Every `Output` module has a
frequency parameter `nint` which specifies the number of time
steps between running the output process.  Many of the routines also
take a `filename` argument to override the default file name
generation, which is most often formed from a combination of the
runtag and the output module name.  Here is a brief description of the
output modules.  For details on the available arguments, please see
the Doxygen generated man pages or the source code itself.

- ``outlog`` produces a simple summary of the running simulation that
  includes the center of mass position and velocities, angular
  momenta, kinetic and potential energies for the total phase space
  and each component separately.  It also lists the wall-clock time
  for each step.  The file name can be specified with the ``filename``
  parameter.

- ``outps, outpsn, outpsp, outpsq, outchkpt, outchkptq`` produce
  phase-space dumps. The first method appends successive dumps to the
  same file.  The second and third methods generate an individual
  sequentially numbered file for each call.  The ``outpsn`` uses a
  native phase-space consolidation routine which gather all phase
  space at the root node before writing.  The ``outpsp`` uses MPI-IO
  to write phase-space files. This will be faster if you have fast,
  parallel network hardware. All of the floating data fields are
  written as 4-byte floats (single precision).

- ``outpsq`` is the parallel version of `outpsp`, it results in split
  PSP files prefixed by ``SPL`` rather than the ``OUT`` for
  ``outps``. This format is recommended for large phase spaces, as it
  can be much faster if your HPC center has a parallel file system.

- ``outchkpt`` is a version of ``outpsp`` that writes floating fields as
  8-byte floats whose primary use is restarting your simulation with
  full information.

- ``outchkptq`` is a version of ``outchkpt`` that writes 8-byte floats in
  ``SPL`` split format. This is the recommended check-point format for
  runs with :math:`N>10^6`

- ``outascii`` emits phase-space snapshots for a single name-specified
  component at regular intervals in ascii format.  Each line contains:
  ``mass, pos[3], vel[3], acc[3], pot, potext``, followed by the
  attribute arrays ``ival[niattr], dval[ndattr]``. Like ``outpsn``, each
  snapshot is written into a file with a sequentially increasing
  counter.

- ``outcoef`` writes the basis coefficients in binary
  format for the specified component at the desired frequency
  ``nint``.

- ``outfrac`` provides the radius containing the specified mass fraction
  for each specified component and frequency.  This method will work
  for any component but makes the most sense for near-equilibrium
  galaxy components such as disks, bulges and halos.

- ``orbtrace`` will output a select number of orbits to the same file,
  appending phase space information to the end at each time step. This
  is helpful for quick looks, but is not meant to be science product
  output (i.e. one should probably not try to set ``orbtrace`` to the
  number of disk particles).

.. note::
   The ``SPL`` and ``OUT`` prefixes are for humans.  EXP does not use
   these names to distinguish between ``SPL`` and ``OUT`` files.

An example
----------

.. index: pair: configuation; example

We provided a simple example of output stanzas in :ref:`the sample
YAML config <yamlconfig>`.
Here is a more complex specification with a bit of additional
explanation:

.. code-block:: yaml

   Output:
     - id : outlog
       parameters : {nint : 1}
     - id : outpsn
       parameters : {nint : 10}
     - id : outchkpt
       parameters : {nint : 100}
     - id : outcoef
       parameters : {filename : outcoef.star, name : star, nint : 1}
     - id : outcoef
       parameters : {filename : outcoef.dark, name : dark, nint : 1}

For the first three output types, `nint=xx` is the time-step
frequency for output.  EXP will write basic global diagnostics at
every step, will write standard (low-precision) phase-space dumps
after each 10 steps and a high-precision phase-space dump suitable for
a restart after every 100 steps.  In addition, coefficient files will
be saved for a disk component named `star` and a halo component
named `dark` after every step into files named
`outcoef.star` and `outcoef.dark`, respectively.


Adding new output routines
--------------------------

.. index: extending EXP

In short, the steps are as follows.  Suppose that you want a new
output routine that we will call `OutTest`.

- Begin with one of the existing output routines (e.g. `OutLog`) and
  rename both the corresponding `OutTest.H` and `OutTest.cc` file for
  your use.

- Change the name of class to `OutTest` inside the source files and
  add your new functionality.

- Add the `#include <OutText.H>` to the top `OutputContainer.cc` and
  also add a parsing stanza that will create a new instance of your
  output class following the example for `OutLog`.

- Add the `OutText.cc` to the `exp_SOURCES` list
  inside of `CMakeLists.txt` in the `src`} directory.

- Compile, test, and debug as necessary.
